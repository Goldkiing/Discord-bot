import discord from discord.ext import commands from discord import app_commands import json import os import difflib import random import re from textblob import TextBlob import nltk import numpy as np from sentence_transformers import SentenceTransformer from sklearn.metrics.pairwise import cosine_similarity

------------------- Configuration -------------------

MODEL_NAME = 'all-MiniLM-L6-v2' VECTOR_FILE = 'brain_vectors.json' DATA_FILE = 'brain.json' SETTINGS_FILE = 'settings.json' SIMILARITY_THRESHOLD = 0.6

------------------- NLTK Setup -------------------

try: nltk.data.find('tokenizers/punkt') except LookupError: nltk.download('punkt')

try: nltk.data.find('taggers/averaged_perceptron_tagger') except LookupError: nltk.download('averaged_perceptron_tagger')

------------------- Bot Setup -------------------

intents = discord.Intents.default() intents.message_content = True intents.guilds = True bot = commands.Bot(command_prefix='!', intents=intents) tree = bot.tree

------------------- Load Data Safely -------------------

def load_json(path, default): try: if os.path.exists(path): with open(path, 'r', encoding='utf-8') as f: return json.load(f) except Exception as e: print(f"Error loading {path}: {e}") return default

brain = load_json(DATA_FILE, {}) vectors_data = load_json(VECTOR_FILE, {}) settings = load_json(SETTINGS_FILE, {"allowed_users": [], "learn_channels": [], "reply_channels": []})

Ensure backward compatibility

for q, data in list(brain.items()): if isinstance(data, list): brain[q] = {"answers": data, "intent": "unknown"}

embedder = SentenceTransformer(MODEL_NAME)

Convert loaded vectors to numpy arrays

for q, vec in vectors_data.items(): vectors_data[q] = np.array(vec)

------------------- Save Helpers -------------------

def save_brain(): with open(DATA_FILE, 'w', encoding='utf-8') as f: json.dump(brain, f, indent=2, ensure_ascii=False)

def save_vectors(): with open(VECTOR_FILE, 'w', encoding='utf-8') as f: json.dump({q: vec.tolist() for q, vec in vectors_data.items()}, f, indent=2)

def save_settings(): with open(SETTINGS_FILE, 'w', encoding='utf-8') as f: json.dump(settings, f, indent=2)

------------------- Intent Detection -------------------

intent_examples = { "info": ["ما هي سرعة الضوء", "اشرح الذكاء الاصطناعي"], "command": ["افتح الباب", "احذف الرسالة"], "joke": ["قل لي نكتة", "نكتة عن القطط"], "definition": ["ما هو تعريف العلم", "عرف كلمة كذا"], "warning": ["انتبه", "تحذير عاجل"], "motivation": ["أعطني تحفيز", "كلمات مشجعة"], "question": ["لماذا السماء زرقاء", "هل تعرف أين أنا؟"], "personal": ["من أنت", "ما اسمك"] }

intent_embeddings = {}

for intent, examples in intent_examples.items(): emb = np.mean([embedder.encode(e) for e in examples], axis=0) intent_embeddings[intent] = emb

def detect_intent(text): text_vec = embedder.encode(text) similarities = {k: cosine_similarity([text_vec], [v])[0][0] for k, v in intent_embeddings.items()} best_intent = max(similarities, key=similarities.get) return best_intent

------------------- Embedding Helpers -------------------

def get_embedding(text: str): return embedder.encode(text)

for question in brain.keys(): if question not in vectors_data: vectors_data[question] = get_embedding(question)

save_vectors()

------------------- Authorization Check -------------------

def is_authorized(interaction: discord.Interaction): username = str(interaction.user) if username in settings["allowed_users"]: return True if interaction.guild and interaction.user.id == interaction.guild.owner_id: return True return False

------------------- Bot Events -------------------

@bot.event async def on_ready(): await tree.sync() print(f"✅ Logged in as {bot.user}")

------------------- Slash Commands -------------------

@tree.command(name='learn', description='Teach the bot a question and answer.') @app_commands.describe(pair='Format: question => answer') async def learn(interaction: discord.Interaction, pair: str): if interaction.channel.id not in settings["learn_channels"]: await interaction.response.send_message("❌ This channel is not authorized for learning commands.") return try: question, answer = pair.split('=>') question = question.strip().lower() answer = answer.strip() intent = detect_intent(question)

if question in brain:
        if answer not in brain[question]['answers']:
            brain[question]['answers'].append(answer)
    else:
        brain[question] = {"answers": [answer], "intent": intent}

    vectors_data[question] = get_embedding(question)
    save_brain()
    save_vectors()

    await interaction.response.send_message(f"✅ Learned: '{question}' → '{answer}' (intent: {intent})")
except Exception:
    await interaction.response.send_message("❌ Format error! Use: question => answer")

------------------- Message Handling -------------------

@bot.event async def on_message(message: discord.Message): if message.author.bot or message.content.startswith("/"): return if message.channel.id not in settings["reply_channels"]: return

msg = message.content.strip().lower()
corrected = str(TextBlob(msg).correct()).lower()
numbers = re.findall(r"\d+(\.\d+)?", corrected)

if corrected in brain:
    await message.channel.send(f"🤖 {random.choice(brain[corrected]['answers'])}")
    return

match = difflib.get_close_matches(corrected, brain.keys(), n=1, cutoff=0.75)
if match:
    await message.channel.send(f"🤖 {random.choice(brain[match[0]]['answers'])}")
    return

query_emb = get_embedding(corrected).reshape(1, -1)
stored_qs = list(vectors_data.keys())
stored_embs = np.array([vectors_data[q] for q in stored_qs])
cos_scores = cosine_similarity(query_emb, stored_embs)[0]
top_idx = int(np.argmax(cos_scores))
top_score = float(cos_scores[top_idx])

if top_score >= SIMILARITY_THRESHOLD:
    best_q = stored_qs[top_idx]
    await message.channel.send(f"🤖 {random.choice(brain[best_q]['answers'])}")
    return

# Word-based fallback
words = corrected.split()
for q in brain:
    if any(w in q for w in words):
        ans = random.choice(brain[q]['answers'])
        await message.channel.send(f"🤖 {ans}\n✅ Learned automatically: '{corrected}' → '{ans}'")
        intent = detect_intent(corrected)
        if corrected not in brain:
            brain[corrected] = {"answers": [ans], "intent": intent}
            vectors_data[corrected] = get_embedding(corrected)
            save_brain()
            save_vectors()
        elif ans not in brain[corrected]['answers']:
            brain[corrected]['answers'].append(ans)
            save_brain()
        return

if numbers:
    await message.channel.send(f"🔢 You mentioned a number: {', '.join(numbers)}")

await bot.process_commands(message)

------------------- Run Bot -------------------

bot.run('MTM5MDQ2NjcwOTc5MzgwMDM3Mw.GXhuge.4ybm7H7QMsGeKnY38HHQfqCXlFr0Hd54rMAPZo')

