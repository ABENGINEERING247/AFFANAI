import os
import re
import random
import streamlit as st

st.set_page_config(page_title="AFFAN AI | Kids' Companion", page_icon="🤖", layout="wide")

# AFFAN AI — child-focused bilingual discovery assistant.
# Optional: set OPENAI_API_KEY and OPENAI_MODEL in Streamlit secrets to enable AI-generated
# explanations. Curated links remain the primary discovery path; external video content
# is not guaranteed safe, so adult supervision and platform parental controls are advised.

st.markdown("""
<style>
:root { color-scheme: light; }
.block-container {padding-top: 1.3rem; max-width: 1120px;}
.hero {background: linear-gradient(120deg,#e9fff8,#eef5ff); border:1px solid #d5eee8;
       border-radius:24px; padding:24px; margin-bottom:18px;}
.robot {font-size:64px; line-height:1;}
.pill {display:inline-block; padding:5px 10px; border-radius:20px;
       background:#ffffff; border:1px solid #dbe9e7; margin:3px; font-size:13px;}
.resource {border:1px solid #e3e9ef; border-radius:16px; padding:16px; height:100%;}
.small {font-size:13px; color:#5f6b76;}
.stButton>button {border-radius:12px; min-height:44px;}
</style>
""", unsafe_allow_html=True)

LANGS = ["English", "اردو", "Roman Urdu"]
TEXT = {
    "English": {
        "tag": "Your friendly cartoon, learning & story buddy!",
        "hello": "Hi, superstar! 🌟 Tell me what you want to do, and I'll suggest child-friendly ideas and links.",
        "task": "What would you like to do today?",
        "placeholder": "e.g. Find Urdu cartoons about animals, help me learn fractions, or tell me a bedtime story...",
        "send": "Find ideas for me ✨",
        "age": "Child's age group",
        "language": "Chat language",
        "parent": "Parent / caregiver",
        "safety": "AFFAN is designed for children. Ask a parent before opening links, sharing information, or watching a movie.",
        "recommend": "Ideas for you",
        "watch": "Watch / explore",
        "book": "Books & reading",
        "learn": "Learn & create",
        "chat": "Chat with Affan",
        "privacy": "Please do not enter your full name, address, school, phone number, password, or private photos.",
        "adult": "I can only help with child-friendly topics. Let's choose a safe activity, story, cartoon, or learning task instead.",
        "need": "Try describing your task in a little more detail.",
        "parent_controls": "Parent safety settings",
        "safe_mode": "Child-safe discovery mode",
        "safe_mode_help": "Keeps recommendations focused on children's learning and entertainment. It cannot guarantee that every external page or video is safe.",
    },
    "اردو": {
        "tag": "کارٹون، تعلیم اور کہانیوں کا آپ کا دوستانہ ساتھی!",
        "hello": "السلام علیکم، ننھے دوست! 🌟 بتائیں آج آپ کیا کرنا چاہتے ہیں؟ میں بچوں کے لیے مناسب سرگرمیاں اور لنکس تجویز کروں گا۔",
        "task": "آج آپ کیا کرنا چاہتے ہیں؟",
        "placeholder": "مثلاً جانوروں کے اردو کارٹون، ریاضی میں مدد، یا سونے سے پہلے ایک کہانی...",
        "send": "میرے لیے تجاویز دیں ✨",
        "age": "بچے کی عمر",
        "language": "گفتگو کی زبان",
        "parent": "والدین / سرپرست",
        "safety": "AFFAN بچوں کے لیے بنایا گیا ہے۔ لنک کھولنے، ذاتی معلومات دینے یا فلم دیکھنے سے پہلے والدین سے اجازت لیں۔",
        "recommend": "آپ کے لیے تجاویز",
        "watch": "دیکھیں / تلاش کریں",
        "book": "کتابیں اور مطالعہ",
        "learn": "سیکھیں اور بنائیں",
        "chat": "AFFAN سے بات کریں",
        "privacy": "اپنا پورا نام، پتہ، اسکول، فون نمبر، پاس ورڈ یا ذاتی تصاویر یہاں نہ لکھیں۔",
        "adult": "میں صرف بچوں کے لیے مناسب موضوعات میں مدد کر سکتا ہوں۔ آئیں کوئی محفوظ سرگرمی، کہانی، کارٹون یا تعلیمی کام منتخب کریں۔",
        "need": "اپنے کام کی تھوڑی مزید وضاحت کریں۔",
        "parent_controls": "والدین کی حفاظتی ترتیبات",
        "safe_mode": "بچوں کے لیے محفوظ تجاویز",
        "safe_mode_help": "تجاویز بچوں کی تعلیم اور تفریح تک محدود رکھنے کی کوشش کرتا ہے۔ بیرونی ویب سائٹس یا ویڈیوز کی مکمل حفاظت کی ضمانت نہیں دی جا سکتی۔",
    },
    "Roman Urdu": {
        "tag": "Cartoons, taleem aur kahaniyon ka dost!",
        "hello": "Assalam-o-alaikum, little star! 🌟 Batao aaj kya karna hai? Main bachon ke liye munasib activities aur links suggest karunga.",
        "task": "Aaj aap kya karna chahte hain?",
        "placeholder": "Misal: janwaron ke Urdu cartoons, fractions seekhna, ya bedtime story...",
        "send": "Mere liye ideas dhoondo ✨",
        "age": "Bachay ki age",
        "language": "Chat ki zaban",
        "parent": "Parent / guardian",
        "safety": "AFFAN bachon ke liye hai. Links kholne, personal info dene ya movie dekhne se pehle parent se poochhein.",
        "recommend": "Aap ke liye ideas",
        "watch": "Dekhein / explore karein",
        "book": "Books aur reading",
        "learn": "Seekhein aur banayein",
        "chat": "Affan se baat karein",
        "privacy": "Apna poora naam, address, school, phone, password ya private photos yahan share na karein.",
        "adult": "Main sirf bachon ke liye munasib topics mein madad kar sakta hoon. Chaliye koi safe activity, story, cartoon ya learning task chunte hain.",
        "need": "Apne task ki thori aur tafseel likhein.",
        "parent_controls": "Parent safety settings",
        "safe_mode": "Kids-safe discovery mode",
        "safe_mode_help": "Yeh suggestions ko bachon ki learning aur entertainment par focus karta hai. Har external website/video ki safety ki guarantee nahi.",
    }
}

# Curated starting points. Prefer official channels/sites where known.
RESOURCES = [
    {"title":"KidsLand Pakistan", "kind":"Urdu cartoons & moral stories",
     "url":"https://kidsland.com.pk/", "tags":["cartoon","urdu","story","islamic","pakistan","moral","video","movie"],
     "desc":"Pakistani Urdu cartoons, poems and family-value stories."},
    {"title":"KidsLand Official on YouTube", "kind":"Urdu cartoon videos",
     "url":"https://www.youtube.com/@KidsLandOfficial", "tags":["cartoon","urdu","video","ghulam rasool","kaneez fatima","story"],
     "desc":"Official channel for children's animated series and stories."},
    {"title":"Kids Madani Channel", "kind":"Children's learning & Urdu videos",
     "url":"https://www.youtube.com/results?search_query=Kids+Madani+Channel+official+kids", "tags":["islamic","urdu","nazam","story","learning","video"],
     "desc":"Explore Urdu children's learning, stories and poems; review each video with a parent."},
    {"title":"Taleemabad", "kind":"Educational learning",
     "url":"https://taleemabad.com/", "tags":["homework","math","science","school","learning","english","urdu","education"],
     "desc":"Explore school-oriented learning resources."},
    {"title":"Pakistan National Book Foundation", "kind":"Books & reading",
     "url":"https://www.nbf.org.pk/", "tags":["book","books","reading","urdu","english","study","story"],
     "desc":"A starting point for finding books and reading resources."},
    {"title":"NASA Space Place", "kind":"Science for kids",
     "url":"https://spaceplace.nasa.gov/", "tags":["science","space","planet","moon","rocket","stars","astronomy"],
     "desc":"Space, Earth and science activities for curious children."},
    {"title":"National Geographic Kids", "kind":"Animals & nature",
     "url":"https://kids.nationalgeographic.com/", "tags":["animal","animals","nature","ocean","dinosaur","science","geography"],
     "desc":"Explore animals, nature and the world; parent guidance recommended."},
    {"title":"Khan Academy Kids", "kind":"Early learning",
     "url":"https://learn.khanacademy.org/khan-academy-kids/", "tags":["math","reading","letters","numbers","learning","homework","english"],
     "desc":"Early-learning activities and educational practice."},
    {"title":"Storynory", "kind":"Audio stories",
     "url":"https://www.storynory.com/", "tags":["story","stories","bedtime","fairy tale","audio","reading"],
     "desc":"Children's audio stories; a parent should review the selection."},
    {"title":"YouTube Kids", "kind":"Kids video platform",
     "url":"https://www.youtubekids.com/", "tags":["cartoon","video","movie","poem","nazam","music","kids"],
     "desc":"Use with parent-managed settings and supervision; filters are not perfect."},
    {"title":"Urdu cartoon search", "kind":"Video search",
     "url":"https://www.youtube.com/results?search_query=Urdu+cartoons+for+kids+official", "tags":["cartoon","urdu","video","movie"],
     "desc":"Search results can include unsuitable uploads. Choose official channels with a parent."},
    {"title":"Urdu bedtime stories", "kind":"Story videos",
     "url":"https://www.youtube.com/results?search_query=Urdu+bedtime+stories+for+kids+official", "tags":["story","bedtime","urdu","video","fairy tale"],
     "desc":"Find Urdu stories and review the exact video before watching."},
    {"title":"Kids' drawing ideas", "kind":"Art & creativity",
     "url":"https://www.youtube.com/results?search_query=easy+drawing+for+kids+official+educational", "tags":["draw","drawing","art","colour","color","craft","creative"],
     "desc":"Creative drawing ideas; use child-safe materials."},
]

# Lightweight topic screening; not a substitute for proper moderation or parental supervision.
BLOCK_PATTERNS = [
    r"\b(porn|pornography|nude|naked|sex|sexual|erotic|adult movie|18\+|xxx)\b",
    r"\b(gore|graphic violence|torture|suicide|self[- ]?harm|how to make a weapon|bomb making)\b",
]
PRIVATE_PATTERNS = [
    r"\b(my password is|my home address is|my phone number is|my credit card)\b"
]
CHILD_TASKS = {
    "math": ["math", "fraction", "addition", "subtraction", "multiplication", "division", "algebra", "ریاضی", "jama", "taqseem"],
    "science": ["science", "planet", "space", "rocket", "experiment", "سائنس", "sayara"],
    "cartoon": ["cartoon", "movie", "film", "animation", "video", "کارٹون", "فلم"],
    "story": ["story", "stories", "kahani", "کہانی", "bedtime", "fairy tale"],
    "book": ["book", "books", "reading", "novel", "کتاب", "مطالعہ"],
    "animal": ["animal", "animals", "dinosaur", "ocean", "janwar", "جانور"],
    "art": ["draw", "drawing", "art", "craft", "colour", "color", "رسم", "تصویر"],
    "urdu": ["urdu", "اردو", "nazam", "poem", "poetry", "نظم"],
    "islamic": ["islam", "islamic", "dua", "prophet", "namaz", "اسلام", "دعا"],
}

def screen_task(task):
    low = task.lower()
    if any(re.search(p, low, re.I) for p in BLOCK_PATTERNS):
        return "blocked"
    if any(re.search(p, low, re.I) for p in PRIVATE_PATTERNS):
        return "private"
    return "ok"

def choose_resources(task, limit=6):
    low = task.lower()
    scored = []
    for item in RESOURCES:
        score = sum(1 for tag in item["tags"] if tag.lower() in low)
        if score:
            scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    chosen = [x[1] for x in scored[:limit]]
    if not chosen:
        chosen = [RESOURCES[0], RESOURCES[3], RESOURCES[8], RESOURCES[9]]
    # Deduplicate by URL.
    seen, result = set(), []
    for item in chosen:
        if item["url"] not in seen:
            result.append(item); seen.add(item["url"])
    return result

def bilingual_reply(task, lang, age):
    status = screen_task(task)
    if status == "blocked":
        return TEXT[lang]["adult"], []
    if status == "private":
        return TEXT[lang]["privacy"], []
    if len(task.strip()) < 3:
        return TEXT[lang]["need"], []
    resources = choose_resources(task)
    if lang == "اردو":
        reply = f"زبردست! 🌟 آپ کے کام کے لیے یہ بچوں کے لیے مناسب آغاز ہو سکتا ہے۔ عمر کا گروپ: {age}۔ لنک کھولنے سے پہلے والدین سے مدد لیں اور ویڈیو خود چیک کروائیں۔"
    elif lang == "Roman Urdu":
        reply = f"Shabash! 🌟 Aap ke task ke liye yeh achay starting points hain. Age group: {age}. Link kholne se pehle parent se help lein aur video check karwa lein."
    else:
        reply = f"Great idea! 🌟 Here are some starting points for your task. Age group: {age}. Ask a parent to check each video or page before you open it."
    return reply, resources

with st.sidebar:
    st.markdown("## 🤖 AFFAN AI")
    st.caption("Made for children • Pakistan")
    lang = st.selectbox("Chat language / گفتگو کی زبان", LANGS, index=0)
    age = st.selectbox(TEXT[lang]["age"], ["Under 6", "6–8", "9–12", "13–15"])
    with st.expander(TEXT[lang]["parent_controls"], expanded=True):
        st.info(TEXT[lang]["safe_mode_help"])
        parent_pin = st.text_input("Parent PIN (optional local session)", type="password",
                                   help="This demo does not store or verify a secure parent PIN.")
        st.checkbox("I am a parent / caregiver", value=False, key="parent_confirm")
        st.caption("For real deployments, add server-side parental authentication, moderation, logging controls and a curated allowlist.")
    st.markdown("---")
    st.caption("Privacy tip: don't share personal information with any chatbot.")

st.markdown(f"""
<div class="hero">
  <div class="robot">🤖🍿📚</div>
  <h1 style="margin:6px 0 4px;color:#163b56">AFFAN AI</h1>
  <h3 style="margin:0 0 8px;color:#168b78">Kids' Learning, Cartoons & Stories</h3>
  <p style="font-size:17px;margin-bottom:10px">{TEXT[lang]["tag"]}</p>
  <span class="pill">🇵🇰 Pakistan-focused</span>
  <span class="pill">اردو</span>
  <span class="pill">English</span>
  <span class="pill">Roman Urdu</span>
</div>
""", unsafe_allow_html=True)

st.info(TEXT[lang]["safety"])
tab_chat, tab_discover, tab_parent = st.tabs(["💬 " + TEXT[lang]["chat"], "🎬 " + TEXT[lang]["watch"], "🛡️ Parent guide"])

with tab_chat:
    st.subheader(TEXT[lang]["task"])
    st.write(TEXT[lang]["hello"])
    with st.form("task_form", clear_on_submit=False):
        task = st.text_area("Your task / آپ کا کام", placeholder=TEXT[lang]["placeholder"], height=110)
        submitted = st.form_submit_button(TEXT[lang]["send"], use_container_width=True)
    if submitted:
        reply, links = bilingual_reply(task, lang, age)
        st.session_state["last_task"] = task
        st.session_state["last_reply"] = reply
        st.session_state["last_links"] = links
    if st.session_state.get("last_reply"):
        st.markdown("### " + TEXT[lang]["recommend"])
        st.write(st.session_state["last_reply"])
        links = st.session_state.get("last_links", [])
        if links:
            cols = st.columns(2)
            for i, item in enumerate(links):
                with cols[i % 2]:
                    st.markdown(f"""<div class="resource"><h4>{item['title']}</h4>
                    <p><b>{item['kind']}</b></p><p>{item['desc']}</p>
                    <p><a href="{item['url']}" target="_blank" rel="noopener noreferrer">Open resource ↗</a></p>
                    </div>""", unsafe_allow_html=True)
        st.caption(TEXT[lang]["privacy"])

with tab_discover:
    st.subheader("Explore children's resources / بچوں کے لیے مواد")
    query = st.text_input("Search by topic / موضوع تلاش کریں", placeholder="Urdu cartoons, science, books, bedtime stories...")
    if query:
        found = choose_resources(query, limit=10)
    else:
        found = RESOURCES[:10]
    for item in found:
        with st.container(border=True):
            st.markdown(f"**{item['title']}** · {item['kind']}")
            st.write(item["desc"])
            st.markdown(f"[Open resource ↗]({item['url']})")

with tab_parent:
    st.subheader("A safer way for children to explore")
    st.markdown("""
- Use a child profile and turn on platform-level parental controls.
- Prefer official publishers and channels. Search results and recommendations can contain unsuitable material.
- Review films and books yourself; age ratings and cultural suitability vary.
- Keep devices in shared family spaces for younger children.
- Do not collect children's full names, school details, exact location, photos, passwords, or private conversations.
- If adding an AI API, use server-side secrets, moderation, rate limits, and a reviewed child-safe system prompt.
- For a production app, add a parent PIN that is securely verified server-side; this demo's optional field is not real authentication.
""")
    st.markdown("**Pakistan child-safety resources**")
    st.markdown("- [Pakistan National CERT — Cyber Care for Children](https://pkcert.gov.pk/ccc-program.asp)")
    st.markdown("- [NCCIA — Cyber Safety](https://www.nccia.gov.pk/cyber-safety.php)")
    st.markdown("- [National Commission on the Rights of Child — Parent guide](https://ncrc.gov.pk/wp-content/uploads/2025/03/A-Guide-to-Parental-Control-by-PTA-A5.pdf)")

st.markdown("---")
st.caption("AFFAN AI • A child-focused discovery prototype. External links may change, and no chatbot can guarantee that third-party content is always safe. Parent supervision is essential.")
