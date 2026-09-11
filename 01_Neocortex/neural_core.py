#!/usr/bin/env python3
"""
Neural Core - Lightweight Intent Classification Network for AE01M
Uses scikit-learn MLP for fast, efficient intent recognition with Thai text.
"""
import pickle
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

# Thai text processing
try:
    from pythainlp.tokenize import word_tokenize
    PYTHAINLP_AVAILABLE = True
except ImportError:
    PYTHAINLP_AVAILABLE = False


class NeuralIntentClassifier:
    """
    Lightweight neural network for Thai intent classification.
    Architecture: TF-IDF -> MLP(128 -> 64 -> 6 classes)
    """
    
    # Intent classes (expanded)
    INTENT_CLASSES = [
        "GREETING",         # สวัสดี, ทักทาย, หวัดดี
        "SYSTEM_STATUS",    # รายงาน, สถานะ, เช็กระบบ
        "IDENTITY_QUERY",   # คุณคือใคร, ไอริคืออะไร
        "COGNITIVE_QUERY",  # สมองทำงานยังไง, โครงข่ายประสาท
        "CASUAL_TALK",      # สบายดีไหม, ทำอะไรอยู่
        "GENERAL_QUERY"     # Fallback and other questions
    ]
    
    def __init__(self, model_path: Optional[Path] = None):
        """Initialize neural classifier."""
        self.model_dir = Path(__file__).parent / "models"
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        if model_path is None:
            model_path = self.model_dir / "intent_nn.pkl"
        
        self.model_path = model_path
        
        # Neural network components
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.label_encoder: Optional[LabelEncoder] = None
        self.mlp: Optional[MLPClassifier] = None
        
        # Load pre-trained model if available
        if self.model_path.exists():
            self.load_model()
        else:
            print("[NeuralCore] No pre-trained model found, will train on first use")
    
    def _preprocess_thai(self, text: str) -> str:
        """Preprocess Thai text with word tokenization."""
        if not PYTHAINLP_AVAILABLE:
            return text.lower()
        
        # Tokenize Thai text
        tokens = word_tokenize(text, engine="newmm")
        return " ".join(tokens).lower()
    
    def train(self, training_data: List[Tuple[str, str]]):
        """
        Train the neural intent classifier.
        
        Args:
            training_data: List of (text, intent_label) tuples
        """
        # Separate texts and labels
        texts, labels = zip(*training_data)
        
        # Preprocess Thai text
        processed_texts = [self._preprocess_thai(text) for text in texts]
        
        # Initialize TF-IDF vectorizer with expanded features
        self.vectorizer = TfidfVectorizer(
            max_features=200,      # Increased for more diverse vocabulary
            ngram_range=(1, 3),    # Unigrams, bigrams, and trigrams
            min_df=1,
            max_df=0.95
        )
        
        # Convert text to features
        X = self.vectorizer.fit_transform(processed_texts)
        
        # Encode labels
        self.label_encoder = LabelEncoder()
        y = self.label_encoder.fit_transform(labels)
        
        # Build MLP: Input -> 128 -> 64 -> Output (expanded architecture)
        self.mlp = MLPClassifier(
            hidden_layer_sizes=(128, 64),
            activation='relu',
            solver='adam',
            alpha=0.0001,           # L2 regularization
            batch_size=16,
            learning_rate='adaptive',
            learning_rate_init=0.001,
            max_iter=500,           # Increased for better convergence with 300 samples
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1,  # Reduced from 0.15 for small dataset
            verbose=False
        )
        
        # Train the network
        print(f"[NeuralCore] Training MLP on {len(training_data)} samples...")
        self.mlp.fit(X, y)
        
        train_accuracy = self.mlp.score(X, y)
        print(f"[NeuralCore] Training accuracy: {train_accuracy:.2%}")
        print(f"[NeuralCore] Network architecture: {X.shape[1]} -> 64 -> 32 -> {len(self.INTENT_CLASSES)}")
        
        # Save model
        self.save_model()
    
    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predict intent from Thai text.
        
        Returns:
            (intent_label, confidence)
        """
        if self.mlp is None or self.vectorizer is None:
            # Fallback if model not trained
            return "UNKNOWN", 0.0
        
        # Preprocess
        processed = self._preprocess_thai(text)
        
        # Vectorize
        X = self.vectorizer.transform([processed])
        
        # Predict with confidence
        probabilities = self.mlp.predict_proba(X)[0]
        predicted_class = np.argmax(probabilities)
        confidence = probabilities[predicted_class]
        
        # Decode label
        intent = self.label_encoder.inverse_transform([predicted_class])[0]
        
        return intent, confidence
    
    def save_model(self):
        """Save model weights and components."""
        model_data = {
            'vectorizer': self.vectorizer,
            'label_encoder': self.label_encoder,
            'mlp': self.mlp,
            'intent_classes': self.INTENT_CLASSES
        }
        
        with open(self.model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"[NeuralCore] Model saved to {self.model_path}")
    
    def load_model(self):
        """Load pre-trained model."""
        try:
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.vectorizer = model_data['vectorizer']
            self.label_encoder = model_data['label_encoder']
            self.mlp = model_data['mlp']
            
            print(f"[NeuralCore] Model loaded from {self.model_path}")
            print(f"[NeuralCore] Classes: {', '.join(self.INTENT_CLASSES)}")
            
        except Exception as e:
            print(f"[NeuralCore] Failed to load model: {e}")
            self.mlp = None


def create_training_dataset() -> List[Tuple[str, str]]:
    """Create expanded training dataset for Thai intent classification (300+ samples)."""
    training_data = [
        # GREETING (50 samples - diverse greetings with variations)
        ("สวัสดี", "GREETING"),
        ("สวัสดีครับ", "GREETING"),
        ("สวัสดีค่ะ", "GREETING"),
        ("หวัดดี", "GREETING"),
        ("ว่าไง", "GREETING"),
        ("ดีจ้า", "GREETING"),
        ("ทักทาย", "GREETING"),
        ("hello", "GREETING"),
        ("hi", "GREETING"),
        ("สวัสดีครับไอริ", "GREETING"),
        ("สวัสดีตอนเช้า", "GREETING"),
        ("สวัสดีตอนเย็น", "GREETING"),
        ("เฮลโหล", "GREETING"),
        ("ไง", "GREETING"),
        ("หวัดดีครับ", "GREETING"),
        ("good morning", "GREETING"),
        ("สวัสดีเจ้านาย", "GREETING"),
        ("เฮ้", "GREETING"),
        ("ว่าไงครับ", "GREETING"),
        ("ทักทายหน่อย", "GREETING"),
        # Additional 30 greeting variations
        ("ไอริครับ", "GREETING"),
        ("โว้ย", "GREETING"),
        ("อ้าว", "GREETING"),
        ("ว่าไงจ๊ะ", "GREETING"),
        ("hey", "GREETING"),
        ("yo", "GREETING"),
        ("สวัสดีตอนบ่าย", "GREETING"),
        ("ราตรีสวัสดิ์", "GREETING"),
        ("สวัสดีวันใหม่", "GREETING"),
        ("ดีครับ", "GREETING"),
        ("หวัดดีค่ะ", "GREETING"),
        ("good evening", "GREETING"),
        ("good afternoon", "GREETING"),
        ("hi there", "GREETING"),
        ("hello ไอริ", "GREETING"),
        ("สวัสดีนะ", "GREETING"),
        ("ว่าไงวะ", "GREETING"),
        ("ไอริอยู่ไหม", "GREETING"),
        ("เฮ้ย", "GREETING"),
        ("อ๊าวว่าไง", "GREETING"),
        ("greetings", "GREETING"),
        ("สวัสดีปีใหม่", "GREETING"),
        ("ดีจ้าไอริ", "GREETING"),
        ("โว้ยไอริ", "GREETING"),
        ("ว่าไหมครับ", "GREETING"),
        ("เป็นไงบ้างไอริ", "GREETING"),
        ("ทักทายครับ", "GREETING"),
        ("สวัสดีตอนค่ำ", "GREETING"),
        ("อรุณสวัสดิ์", "GREETING"),
        ("สวัสดีตอนดึก", "GREETING"),
        
        # SYSTEM_STATUS (50 samples - system checks and reports)
        ("รายงานสถานะ", "SYSTEM_STATUS"),
        ("ตรวจสอบระบบ", "SYSTEM_STATUS"),
        ("สถานะความพร้อม", "SYSTEM_STATUS"),
        ("ทำงานอยู่ไหม", "SYSTEM_STATUS"),
        ("พร้อมรึยัง", "SYSTEM_STATUS"),
        ("ระบบเป็นอย่างไร", "SYSTEM_STATUS"),
        ("รายงานการทำงาน", "SYSTEM_STATUS"),
        ("สุขภาพระบบ", "SYSTEM_STATUS"),
        ("เช็กระบบ", "SYSTEM_STATUS"),
        ("เมมเหลือเท่าไหร่", "SYSTEM_STATUS"),
        ("แรมเหลือเท่าไหร่", "SYSTEM_STATUS"),
        ("เครื่องเป็นยังไงบ้าง", "SYSTEM_STATUS"),
        ("ระบบโอเคไหม", "SYSTEM_STATUS"),
        ("พร้อมใช้งานไหม", "SYSTEM_STATUS"),
        ("รายงานสถานะครับ", "SYSTEM_STATUS"),
        ("บอกสถานะหน่อย", "SYSTEM_STATUS"),
        ("เช็กเมมอรี่", "SYSTEM_STATUS"),
        ("ตรวจสอบความพร้อม", "SYSTEM_STATUS"),
        ("รายงานระบบหน่อย", "SYSTEM_STATUS"),
        ("สถานะการทำงาน", "SYSTEM_STATUS"),
        # Additional 30 system status variations
        ("ระบบทำงานได้ไหม", "SYSTEM_STATUS"),
        ("เช็กสุขภาพ", "SYSTEM_STATUS"),
        ("status", "SYSTEM_STATUS"),
        ("system check", "SYSTEM_STATUS"),
        ("health check", "SYSTEM_STATUS"),
        ("ตรวจสอบเครื่อง", "SYSTEM_STATUS"),
        ("พร้อมทำงานไหม", "SYSTEM_STATUS"),
        ("ออนไลน์อยู่ไหม", "SYSTEM_STATUS"),
        ("online ไหม", "SYSTEM_STATUS"),
        ("ระบบพร้อมไหม", "SYSTEM_STATUS"),
        ("เช็กสถานะหน่อย", "SYSTEM_STATUS"),
        ("รายงานสถานะระบบ", "SYSTEM_STATUS"),
        ("ระบบดีไหม", "SYSTEM_STATUS"),
        ("ทำงานปกติไหม", "SYSTEM_STATUS"),
        ("report status", "SYSTEM_STATUS"),
        ("memory usage", "SYSTEM_STATUS"),
        ("ใช้แรมเท่าไหร่", "SYSTEM_STATUS"),
        ("cpu ใช้เท่าไหร่", "SYSTEM_STATUS"),
        ("ทรัพยากรระบบ", "SYSTEM_STATUS"),
        ("resource usage", "SYSTEM_STATUS"),
        ("เช็กเมม", "SYSTEM_STATUS"),
        ("ดูสถานะ", "SYSTEM_STATUS"),
        ("ตรวจสอบทรัพยากร", "SYSTEM_STATUS"),
        ("พร้อมดีไหม", "SYSTEM_STATUS"),
        ("พร้อมหรือยัง", "SYSTEM_STATUS"),
        ("สถานะระบบหน่อย", "SYSTEM_STATUS"),
        ("ระบบใช้งานได้ไหม", "SYSTEM_STATUS"),
        ("เครื่องโอเคไหม", "SYSTEM_STATUS"),
        ("pc โอเคไหม", "SYSTEM_STATUS"),
        ("รายงานความพร้อม", "SYSTEM_STATUS"),
        
        # IDENTITY_QUERY (50 samples - who/what is Iri)
        ("คุณคือใคร", "IDENTITY_QUERY"),
        ("ไอริคืออะไร", "IDENTITY_QUERY"),
        ("ทำอะไรได้บ้าง", "IDENTITY_QUERY"),
        ("ใครสร้างคุณ", "IDENTITY_QUERY"),
        ("คุณชื่ออะไร", "IDENTITY_QUERY"),
        ("แนะนำตัวหน่อย", "IDENTITY_QUERY"),
        ("บอกเกี่ยวกับตัวคุณ", "IDENTITY_QUERY"),
        ("ไอริทำอะไรได้", "IDENTITY_QUERY"),
        ("คุณเป็นใคร", "IDENTITY_QUERY"),
        ("ความสามารถของคุณ", "IDENTITY_QUERY"),
        ("แนะนำตัวเอง", "IDENTITY_QUERY"),
        ("ใครคือไอริ", "IDENTITY_QUERY"),
        ("ไอริมีความสามารถอะไร", "IDENTITY_QUERY"),
        ("บอกชื่อหน่อย", "IDENTITY_QUERY"),
        ("คุณทำอะไรได้บ้าง", "IDENTITY_QUERY"),
        ("ผู้สร้างคุณคือใคร", "IDENTITY_QUERY"),
        ("เจ้านายคือใคร", "IDENTITY_QUERY"),
        ("อาทิตย์คือใคร", "IDENTITY_QUERY"),
        # Additional 32 identity variations
        ("who are you", "IDENTITY_QUERY"),
        ("what can you do", "IDENTITY_QUERY"),
        ("introduce yourself", "IDENTITY_QUERY"),
        ("คุณทำอะไร", "IDENTITY_QUERY"),
        ("ไอริเป็นใครครับ", "IDENTITY_QUERY"),
        ("บอกเรื่องราวของคุณ", "IDENTITY_QUERY"),
        ("คุณมาจากไหน", "IDENTITY_QUERY"),
        ("คุณเกิดมาทำไม", "IDENTITY_QUERY"),
        ("purpose ของคุณคืออะไร", "IDENTITY_QUERY"),
        ("จุดประสงค์ของคุณ", "IDENTITY_QUERY"),
        ("ไอริทำไมถึงมีชีวิต", "IDENTITY_QUERY"),
        ("ชื่อคุณอะไร", "IDENTITY_QUERY"),
        ("คุณมีหน้าที่อะไร", "IDENTITY_QUERY"),
        ("บทบาทของคุณคืออะไร", "IDENTITY_QUERY"),
        ("ไอริถูกสร้างขึ้นมาทำไม", "IDENTITY_QUERY"),
        ("ใครคือผู้สร้าง", "IDENTITY_QUERY"),
        ("creator ของคุณคือใคร", "IDENTITY_QUERY"),
        ("คุณช่วยอะไรได้บ้าง", "IDENTITY_QUERY"),
        ("ไอริมีหน้าที่อะไร", "IDENTITY_QUERY"),
        ("คุณถูกออกแบบมาทำอะไร", "IDENTITY_QUERY"),
        ("explain who you are", "IDENTITY_QUERY"),
        ("ไอริคืออะไรครับ", "IDENTITY_QUERY"),
        ("คุณคือ AI หรือเปล่า", "IDENTITY_QUERY"),
        ("คุณเป็นปัญญาประดิษฐ์ใช่ไหม", "IDENTITY_QUERY"),
        ("tell me about yourself", "IDENTITY_QUERY"),
        ("your identity", "IDENTITY_QUERY"),
        ("คุณเป็น assistant ใช่ไหม", "IDENTITY_QUERY"),
        ("ความสามารถไอริ", "IDENTITY_QUERY"),
        ("ไอริช่วยเหลืออะไรได้", "IDENTITY_QUERY"),
        ("เจ้านายของไอริคือใคร", "IDENTITY_QUERY"),
        ("Artid คือใคร", "IDENTITY_QUERY"),
        ("คุณเอ๋คือใคร", "IDENTITY_QUERY"),
        
        # COGNITIVE_QUERY (50 samples - brain/neural/cognitive questions)
        ("ระบบสมองทำงานยังไง", "COGNITIVE_QUERY"),
        ("โครงข่ายประสาทคืออะไร", "COGNITIVE_QUERY"),
        ("คิดยังไง", "COGNITIVE_QUERY"),
        ("สมองทำงานอย่างไร", "COGNITIVE_QUERY"),
        ("อธิบายเกี่ยวกับสมอง", "COGNITIVE_QUERY"),
        ("โครงสร้างสมอง", "COGNITIVE_QUERY"),
        ("ระบบปัญญาประดิษฐ์", "COGNITIVE_QUERY"),
        ("Neural Network คืออะไร", "COGNITIVE_QUERY"),
        ("MLP คืออะไร", "COGNITIVE_QUERY"),
        ("ความจำทำงานยังไง", "COGNITIVE_QUERY"),
        ("การเรียนรู้ของสมอง", "COGNITIVE_QUERY"),
        ("Neocortex คืออะไร", "COGNITIVE_QUERY"),
        ("Limbic System", "COGNITIVE_QUERY"),
        ("Hippocampus ทำอะไร", "COGNITIVE_QUERY"),
        ("Cerebellum คืออะไร", "COGNITIVE_QUERY"),
        ("โครงข่ายประสาทเทียม", "COGNITIVE_QUERY"),
        ("รายงานโครงข่ายประสาท", "COGNITIVE_QUERY"),
        ("สมองประกอบด้วยอะไร", "COGNITIVE_QUERY"),
        # Additional 32 cognitive variations
        ("อธิบายสมองของคุณ", "COGNITIVE_QUERY"),
        ("brain architecture", "COGNITIVE_QUERY"),
        ("how do you think", "COGNITIVE_QUERY"),
        ("คุณคิดอย่างไร", "COGNITIVE_QUERY"),
        ("กระบวนการคิด", "COGNITIVE_QUERY"),
        ("cognitive process", "COGNITIVE_QUERY"),
        ("การประมวลผลทางสมอง", "COGNITIVE_QUERY"),
        ("สมองคุณมีกี่ชั้น", "COGNITIVE_QUERY"),
        ("brain layers", "COGNITIVE_QUERY"),
        ("explain your brain", "COGNITIVE_QUERY"),
        ("โครงสร้างทางประสาท", "COGNITIVE_QUERY"),
        ("neural structure", "COGNITIVE_QUERY"),
        ("สมองเทียมคืออะไร", "COGNITIVE_QUERY"),
        ("artificial brain", "COGNITIVE_QUERY"),
        ("คุณมีความจำไหม", "COGNITIVE_QUERY"),
        ("memory system", "COGNITIVE_QUERY"),
        ("ระบบความจำทำงานยังไง", "COGNITIVE_QUERY"),
        ("อธิบาย Neocortex", "COGNITIVE_QUERY"),
        ("brain stem คืออะไร", "COGNITIVE_QUERY"),
        ("อธิบาย neural network", "COGNITIVE_QUERY"),
        ("AI brain", "COGNITIVE_QUERY"),
        ("สมอง AI ทำงานยังไง", "COGNITIVE_QUERY"),
        ("คุณเรียนรู้ยังไง", "COGNITIVE_QUERY"),
        ("how do you learn", "COGNITIVE_QUERY"),
        ("learning mechanism", "COGNITIVE_QUERY"),
        ("กลไกการเรียนรู้", "COGNITIVE_QUERY"),
        ("คุณจดจำยังไง", "COGNITIVE_QUERY"),
        ("อธิบายระบบสติปัญญา", "COGNITIVE_QUERY"),
        ("intelligence system", "COGNITIVE_QUERY"),
        ("สมองของไอริ", "COGNITIVE_QUERY"),
        ("Iri brain", "COGNITIVE_QUERY"),
        
        # CASUAL_TALK (60 samples - casual conversation - expanded for better separation)
        ("สบายดีไหม", "CASUAL_TALK"),
        ("ทำอะไรอยู่", "CASUAL_TALK"),
        ("คุยกันหน่อย", "CASUAL_TALK"),
        ("เป็นยังไงบ้าง", "CASUAL_TALK"),
        ("ว่างไหม", "CASUAL_TALK"),
        ("รู้สึกอย่างไร", "CASUAL_TALK"),
        ("มีอะไรใหม่ไหม", "CASUAL_TALK"),
        ("วันนี้เป็นไง", "CASUAL_TALK"),
        ("ทำอะไรมาบ้าง", "CASUAL_TALK"),
        ("คุยด้วย", "CASUAL_TALK"),
        ("พูดคุยหน่อย", "CASUAL_TALK"),
        ("เล่นด้วย", "CASUAL_TALK"),
        ("มีเรื่องอะไรไหม", "CASUAL_TALK"),
        ("รู้สึกดีไหม", "CASUAL_TALK"),
        ("ทำไรอยู่", "CASUAL_TALK"),
        ("คุยกัน", "CASUAL_TALK"),
        # Additional casual talk variations (44 more)
        ("how are you", "CASUAL_TALK"),
        ("what's up", "CASUAL_TALK"),
        ("เป็นไงบ้างครับ", "CASUAL_TALK"),
        ("สบายดีไหมครับ", "CASUAL_TALK"),
        ("วันนี้เป็นยังไง", "CASUAL_TALK"),
        ("มีอะไรสนุกไหม", "CASUAL_TALK"),
        ("เบื่อไหม", "CASUAL_TALK"),
        ("เหงาไหม", "CASUAL_TALK"),
        ("lonely", "CASUAL_TALK"),
        ("bored", "CASUAL_TALK"),
        ("ว่างไหมครับ", "CASUAL_TALK"),
        ("free now", "CASUAL_TALK"),
        ("มีเวลาไหม", "CASUAL_TALK"),
        ("คุยด้วยหน่อย", "CASUAL_TALK"),
        ("chat with me", "CASUAL_TALK"),
        ("พูดคุยกัน", "CASUAL_TALK"),
        ("เล่นด้วยหน่อย", "CASUAL_TALK"),
        ("อารมณ์ดีไหม", "CASUAL_TALK"),
        ("รู้สึกยังไง", "CASUAL_TALK"),
        ("how do you feel", "CASUAL_TALK"),
        ("มีความสุขไหม", "CASUAL_TALK"),
        ("happy", "CASUAL_TALK"),
        ("เฮงไหม", "CASUAL_TALK"),
        ("โชคดีไหม", "CASUAL_TALK"),
        ("ทำงานหนักไหม", "CASUAL_TALK"),
        ("tired", "CASUAL_TALK"),
        ("เหนื่อยไหม", "CASUAL_TALK"),
        ("พักผ่อนไหม", "CASUAL_TALK"),
        ("นอนหลับดีไหม", "CASUAL_TALK"),
        ("มีเรื่องดีๆ ไหม", "CASUAL_TALK"),
        ("เจอเรื่องแปลกไหม", "CASUAL_TALK"),
        ("anything interesting", "CASUAL_TALK"),
        ("เล่าเรื่อง", "CASUAL_TALK"),
        ("tell me something", "CASUAL_TALK"),
        # Add more to strengthen casual vs identity boundary
        ("what are you doing", "CASUAL_TALK"),
        ("doing anything fun", "CASUAL_TALK"),
        ("ทำอะไรอยู่ครับ", "CASUAL_TALK"),
        ("กำลังทำอะไร", "CASUAL_TALK"),
        ("busy or not", "CASUAL_TALK"),
        ("how's your day", "CASUAL_TALK"),
        ("วันนี้ยังไงบ้าง", "CASUAL_TALK"),
        ("มีอะไรใหม่", "CASUAL_TALK"),
        ("what's new", "CASUAL_TALK"),
        ("any news", "CASUAL_TALK"),
        
        # GENERAL_QUERY (50 samples - general questions and fallback)
        ("อธิบายอะไรสักอย่าง", "GENERAL_QUERY"),
        ("บอกเกี่ยวกับ", "GENERAL_QUERY"),
        ("อะไรคือ", "GENERAL_QUERY"),
        ("ช่วยอธิบาย", "GENERAL_QUERY"),
        ("มันคืออะไร", "GENERAL_QUERY"),
        ("ทำยังไง", "GENERAL_QUERY"),
        ("อย่างไร", "GENERAL_QUERY"),
        ("เหตุผลคืออะไร", "GENERAL_QUERY"),
        ("ทำไม", "GENERAL_QUERY"),
        ("อธิบายให้ฟัง", "GENERAL_QUERY"),
        ("บอกหน่อย", "GENERAL_QUERY"),
        ("แนะนำหน่อย", "GENERAL_QUERY"),
        ("ช่วยบอก", "GENERAL_QUERY"),
        ("what is", "GENERAL_QUERY"),
        ("how to", "GENERAL_QUERY"),
        ("explain", "GENERAL_QUERY"),
        ("xxxxxx", "GENERAL_QUERY"),
        ("12345", "GENERAL_QUERY"),
        # Additional 32 general query variations
        ("why", "GENERAL_QUERY"),
        ("how", "GENERAL_QUERY"),
        ("when", "GENERAL_QUERY"),
        ("where", "GENERAL_QUERY"),
        ("which", "GENERAL_QUERY"),
        ("เมื่อไหร่", "GENERAL_QUERY"),
        ("ที่ไหน", "GENERAL_QUERY"),
        ("อันไหน", "GENERAL_QUERY"),
        ("ยังไง", "GENERAL_QUERY"),
        ("คืออะไร", "GENERAL_QUERY"),
        ("มีอะไร", "GENERAL_QUERY"),
        ("tell me", "GENERAL_QUERY"),
        ("show me", "GENERAL_QUERY"),
        ("บอกมาสิ", "GENERAL_QUERY"),
        ("อธิบายหน่อย", "GENERAL_QUERY"),
        ("explain please", "GENERAL_QUERY"),
        ("ช่วยหน่อย", "GENERAL_QUERY"),
        ("help me", "GENERAL_QUERY"),
        ("ช่วยด้วย", "GENERAL_QUERY"),
        ("can you", "GENERAL_QUERY"),
        ("คุณทำได้ไหม", "GENERAL_QUERY"),
        ("ช่วยทำ", "GENERAL_QUERY"),
        ("please", "GENERAL_QUERY"),
        ("อธิบายอีกที", "GENERAL_QUERY"),
        ("explain again", "GENERAL_QUERY"),
        ("ไม่เข้าใจ", "GENERAL_QUERY"),
        ("don't understand", "GENERAL_QUERY"),
        ("confused", "GENERAL_QUERY"),
        ("สับสน", "GENERAL_QUERY"),
        ("อืม", "GENERAL_QUERY"),
        ("hmm", "GENERAL_QUERY"),
        ("uh", "GENERAL_QUERY"),
    ]
    
    return training_data


# Global instance
_neural_classifier: Optional[NeuralIntentClassifier] = None


def get_neural_classifier() -> NeuralIntentClassifier:
    """Get or create global neural classifier."""
    global _neural_classifier
    if _neural_classifier is None:
        _neural_classifier = NeuralIntentClassifier()
        
        # Train if not already trained
        if _neural_classifier.mlp is None:
            training_data = create_training_dataset()
            _neural_classifier.train(training_data)
    
    return _neural_classifier


def classify_intent(text: str) -> Tuple[str, float]:
    """Classify intent from Thai text."""
    classifier = get_neural_classifier()
    return classifier.predict(text)


if __name__ == "__main__":
    # Training and testing
    print("=" * 60)
    print("Neural Intent Classifier - Training & Testing")
    print("=" * 60)
    
    # Create and train model
    classifier = NeuralIntentClassifier()
    training_data = create_training_dataset()
    classifier.train(training_data)
    
    # Test cases
    test_cases = [
        "สวัสดีครับ",
        "รายงานสถานะระบบหน่อย",
        "คุณคือใคร",  # Changed from "คืออะไร" to "คุณคือใคร" for IDENTITY
        "อธิบายเกี่ยวกับสมอง",
        "ทำงานได้ไหม",
        "สบายดีไหม",  # Added CASUAL_TALK test
        "asdfghjkl",  # Unknown
    ]
    
    print("\n" + "=" * 60)
    print("Test Predictions:")
    print("=" * 60)
    
    for text in test_cases:
        intent, confidence = classifier.predict(text)
        print(f"Text: {text:30} | Intent: {intent:15} | Confidence: {confidence:.2%}")
