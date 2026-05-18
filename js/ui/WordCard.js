class WordCardUI {
    constructor() {
        this.modal = document.getElementById('word-card-modal');
        this.wordIcon = document.getElementById('word-icon');
        this.wordEnglish = document.getElementById('word-english');
        this.wordPhonetic = document.getElementById('word-phonetic');
        this.wordSentence = document.getElementById('word-sentence');
        this.wordOptions = document.getElementById('word-options');
        this.currentWord = null;
        this.onAnswer = null;
    }

    show(wordData, callback) {
        this.currentWord = wordData;
        this.onAnswer = callback;

        this.wordIcon.textContent = wordData.icon;
        this.wordEnglish.textContent = wordData.word;
        this.wordPhonetic.textContent = wordData.phonetic || '';

        let sentence = wordData.sentence;
        const blankIndex = sentence.indexOf('___');
        if (blankIndex !== -1) {
            sentence = sentence.replace('___', '<span class="blank"></span>');
        }
        this.wordSentence.innerHTML = sentence;

        const options = this.generateOptions(wordData);
        this.shuffleArray(options);

        this.wordOptions.innerHTML = '';
        options.forEach(opt => {
            const btn = document.createElement('button');
            btn.className = 'word-option';
            btn.textContent = opt.translation;
            btn.dataset.correct = opt.isCorrect;
            btn.addEventListener('click', () => this.handleAnswer(btn, opt.isCorrect));
            this.wordOptions.appendChild(btn);
        });

        this.modal.classList.remove('hidden');
    }

    generateOptions(wordData) {
        const options = [];
        
        wordData.options.forEach(opt => {
            options.push({ 
                translation: opt, 
                isCorrect: opt === wordData.answer 
            });
        });

        return options;
    }

    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    handleAnswer(btn, isCorrect) {
        const buttons = this.wordOptions.querySelectorAll('.word-option');
        buttons.forEach(b => {
            b.style.pointerEvents = 'none';
            if (b.dataset.correct === 'true') {
                b.classList.add('correct');
                b.textContent = '✓ ' + b.textContent;
            }
        });

        if (!isCorrect) {
            btn.classList.add('wrong');
            btn.textContent = '✗ ' + btn.textContent;
        }

        setTimeout(() => {
            this.hide();
            if (this.onAnswer) {
                this.onAnswer(isCorrect);
            }
        }, 800);
    }

    hide() {
        this.modal.classList.add('hidden');
    }
}

class BossCardUI {
    constructor() {
        this.modal = document.getElementById('boss-card-modal');
        this.bossHpFill = document.getElementById('boss-hp-fill');
        this.bossProgress = document.getElementById('boss-progress');
        this.bossEnglish = document.getElementById('boss-english');
        this.bossTranslation = document.getElementById('boss-translation');
        this.bossOptions = document.getElementById('boss-options');
        this.currentQuestion = null;
        this.currentIndex = 0;
        this.totalQuestions = 3;
        this.onAnswer = null;
        this.onComplete = null;
    }

    show(questions, callback, completeCallback) {
        this.questions = questions;
        this.currentIndex = 0;
        this.totalQuestions = questions.length;
        this.onAnswer = callback;
        this.onComplete = completeCallback;

        this.updateProgress();
        this.showQuestion(this.questions[0]);

        this.modal.classList.remove('hidden');
    }

    updateProgress() {
        const dots = this.bossProgress.querySelectorAll('.boss-dot');
        dots.forEach((dot, i) => {
            dot.classList.remove('active', 'done');
            if (i < this.currentIndex) {
                dot.classList.add('done');
            } else if (i === this.currentIndex) {
                dot.classList.add('active');
            }
        });
    }

    showQuestion(question) {
        this.currentQuestion = question;
        
        this.bossEnglish.textContent = question.sentence;
        this.bossTranslation.textContent = question.translation || '';

        this.bossOptions.innerHTML = '';
        this.shuffleArray(question.options);

        question.options.forEach(opt => {
            const btn = document.createElement('button');
            btn.className = 'word-option';
            btn.textContent = opt;
            btn.dataset.answer = opt;
            btn.addEventListener('click', () => this.handleAnswer(btn, opt === question.answer));
            this.bossOptions.appendChild(btn);
        });
    }

    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    handleAnswer(btn, isCorrect) {
        const buttons = this.bossOptions.querySelectorAll('.word-option');
        buttons.forEach(b => {
            b.style.pointerEvents = 'none';
            if (b.dataset.answer === this.currentQuestion.answer) {
                b.classList.add('correct');
                b.textContent = '✓ ' + b.textContent;
            }
        });

        if (!isCorrect) {
            btn.classList.add('wrong');
            btn.textContent = '✗ ' + btn.textContent;
        }

        setTimeout(() => {
            if (this.onAnswer) {
                this.onAnswer(isCorrect);
            }

            this.currentIndex++;
            this.updateProgress();

            if (this.currentIndex >= this.totalQuestions) {
                setTimeout(() => {
                    this.hide();
                    if (this.onComplete) {
                        this.onComplete(true);
                    }
                }, 500);
            } else {
                this.showQuestion(this.questions[this.currentIndex]);
            }
        }, 1000);
    }

    updateHp(hp) {
        const percent = (hp / this.totalQuestions) * 100;
        this.bossHpFill.style.width = percent + '%';
    }

    hide() {
        this.modal.classList.add('hidden');
    }
}

class LevelCompleteUI {
    constructor() {
        this.modal = document.getElementById('level-complete-modal');
        this.title = document.getElementById('complete-title');
        this.subtitle = document.getElementById('complete-subtitle');
        this.correctCount = document.getElementById('correct-count');
        this.coinsEarned = document.getElementById('coins-earned');
        this.lettersLearned = document.getElementById('letters-learned');
        this.nextBtn = document.getElementById('next-level-btn');
        this.coinRain = document.getElementById('coin-rain');
        this.onNext = null;
    }

    show(data, callback) {
        this.title.textContent = `🎉 ${data.levelName}！`;
        this.subtitle.textContent = `Letter ${data.letter}`;
        this.correctCount.textContent = `${data.correct}/${data.total}`;
        this.coinsEarned.textContent = data.coins;
        this.lettersLearned.textContent = `${data.letter} ✓`;
        this.onNext = callback;

        if (data.levelId === 'L26') {
            this.nextBtn.textContent = '🏆 返回主菜单';
        } else {
            this.nextBtn.textContent = '进入下一关 →';
        }

        this.createCoinRain();

        this.modal.classList.remove('hidden');
        this.nextBtn.onclick = () => {
            this.hide();
            if (this.onNext) {
                this.onNext();
            }
        };
    }

    createCoinRain() {
        this.coinRain.innerHTML = '';
        for (let i = 0; i < 20; i++) {
            const coin = document.createElement('div');
            coin.className = 'falling-coin';
            coin.style.left = Math.random() * 100 + '%';
            coin.style.animationDuration = (1.5 + Math.random() * 2) + 's';
            coin.style.animationDelay = Math.random() * 2 + 's';
            this.coinRain.appendChild(coin);
        }
    }

    hide() {
        this.modal.classList.add('hidden');
    }
}
