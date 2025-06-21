// ---------------------------------------------
// IMPORTS E DEFINIÇÃO DA CLASSE
// ---------------------------------------------
package quiz.core;

// ---------------------------------------------
// CLASSE CENTRAL DE DADOS DO QUIZ
// ---------------------------------------------
public class QuizCore {
    // -------------------
    // ESTRUTURA DE UMA QUESTÃO
    // -------------------
    public static class Question {
        public String question;
        public String[] options;
        public int correctIndex;

        public Question(String question, String[] options, int correctIndex) {
            this.question = question;
            this.options = options;
            this.correctIndex = correctIndex;
        }
    }

    // -------------------
    // FRASES DE FEEDBACK (ACERTO/ERRO)
    // -------------------
    public static String[] frasesAcerto = {
        "Parabéns!", "Mandou bem!", "Acertou em cheio!", "Você é fera!", "Show de bola!",
        "Resposta perfeita!", "Arrasou!", "Incrível!", "Muito bom!", "Você domina!",
        "Espetacular!", "Genial!", "Sensacional!", "Brilhante!", "Você sabe tudo!",
        "Que acerto!", "Isso mesmo!", "Certíssimo!", "Você é demais!", "Resposta top!"
    };
    public static String[] frasesErro = {
        "Foi quase!", "Tente novamente!", "Não desista!", "Quase lá!", "Próxima você acerta!",
        "Continue tentando!", "Não foi dessa vez!", "Erramos às vezes!", "Ainda há chances!", "Não se preocupe!",
        "Faz parte do aprendizado!", "Vamos para a próxima!", "Não foi bem assim...", "Resposta incorreta!", "Ops, errou!",
        "Não é essa!", "Essa estava difícil!", "Não desanime!", "Você consegue na próxima!", "Mais sorte na próxima!"
    };
}
