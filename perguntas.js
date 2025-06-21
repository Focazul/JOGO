const questions = [
    {
        question: "Quantas voltas vai na casquinha?",
        options: [
            "3,5",   // 0 (1ª opção)
            "2,5",   // 1 (2ª opção)
            "4,5",   // 2 (3ª opção)
            "5,5"    // 3 (4ª opção)
        ],
        correctIndex: 0
    },
    {
        question: "Quantos picles vai no BigMac?",
        options: [
            "1", // 0 (1ª opção)
            "2", // 1 (2ª opção)
            "3", // 2 (3ª opção)
            "4"  // 3 (4ª opção)
        ],
        correctIndex: 1
    },
    {
        question: "Qual a temperatura do reservatorio de mix?",
        options: [
            "3° a 6°",   // 0 (1ª opção)
            "2° a 5°",   // 1 (2ª opção)
            "1° a 4°",   // 2 (3ª opção)
            "-18° a -23°"// 3 (4ª opção)
        ],
        correctIndex: 2
    },
    {
        question: "Quantidade de alface em cada lado do BigMac?",
        options: [
            "12g", // 0 (1ª opção)
            "14g", // 1 (2ª opção)
            "20g", // 2 (3ª opção)
            "24g"  // 3 (4ª opção)
        ],
        correctIndex: 0
    },
    {
        question: "Quantas pedras de gelo vai no refrigerante pequena?",
        options: [
            "3",  // 0 (1ª opção)
            "15", // 1 (2ª opção)
            "10", // 2 (3ª opção)
            "5"   // 3 (4ª opção)
        ],
        correctIndex: 3 // 4ª opção (corrigido de 4 para 3)
    },
    {
        question: "Quantas pedras de gelo vai no refrigerante média?",
        options: [
            "3",  // 0 (1ª opção)
            "15", // 1 (2ª opção)
            "10", // 2 (3ª opção)
            "5"   // 3 (4ª opção)
        ],
        correctIndex: 2
    },
    {
        question: "Quantas pedras de gelo vai no refrigerante grande?",
        options: [
            "3",  // 0 (1ª opção)
            "15", // 1 (2ª opção)
            "10", // 2 (3ª opção)
            "5"   // 3 (4ª opção)
        ],
        correctIndex: 1
    },
    {
        question: "Qual tempo de vida da batata na estufa em minutos?",
        options: [
            "7'", // 0 (1ª opção)
            "8'", // 1 (2ª opção)
            "9'", // 2 (3ª opção)
            "6'"  // 3 (4ª opção)
        ],
        correctIndex: 0
    },
    {
        question: "Quantas tiros de cobertura vai no top sunday?",
        options: [
            "4", // 0 (1ª opção)
            "3", // 1 (2ª opção)
            "1", // 2 (3ª opção)
            "2"  // 3 (4ª opção)
        ],
        correctIndex: 3
    },
    {
        question: "Quantas Oz de molho vai no Cheddar?",
        options: [
            "2 Oz",   // 0 (1ª opção)
            "1 Oz",   // 1 (2ª opção)
            "2/3 Oz", // 2 (3ª opção)
            "1/3 Oz"  // 3 (4ª opção)
        ],
        correctIndex: 1 
    }
];

const crowdBg = document.getElementById('crowd-bg');

function showFeedback(isCorrect, points) {
    feedbackContainer.classList.remove('hidden');

    // Remove classes antigas
    document.body.classList.remove('bg-happy', 'bg-sad');

    // Plateia reage
    if (isCorrect) {
        document.body.classList.add('bg-happy');
    } else {
        document.body.classList.add('bg-sad');
    }

    if (isCorrect) {
        answerFeedback.textContent = 'Correto!';
        answerFeedback.className = 'text-2xl font-bold mb-2 text-green-600';
        pointsEarned.textContent = points;
        pointsEarned.parentElement.classList.add('score-animation');
    } else {
        answerFeedback.textContent = 'Incorreto!';
        answerFeedback.className = 'text-2xl font-bold mb-2 text-red-600';
        pointsEarned.textContent = '0';
    }

    setTimeout(() => {
        pointsEarned.parentElement.classList.remove('score-animation');
        document.body.classList.remove('bg-happy', 'bg-sad');
    }, 1500);
}
