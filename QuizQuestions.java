// ---------------------------------------------
// IMPORTS E DEFINIÇÃO DA CLASSE
// ---------------------------------------------
package quiz.questions;

import quiz.core.QuizCore.Question;
import java.util.*;

// ---------------------------------------------
// LISTA DE QUESTÕES DO QUIZ
// ---------------------------------------------
public class QuizQuestions {
    // -------------------
    // QUESTÕES (Pergunta, Opções, Resposta Correta)
    // -------------------
    public static List<Question> questions = Arrays.asList(
        new Question("Quantas voltas vai na casquinha?",
            new String[]{"3,5", "2,5", "4,5", "5,5"}, 0),
        new Question("Quantos picles vai no BigMac?",
            new String[]{"1", "2", "3", "4"}, 1),
        new Question("Qual a temperatura do reservatorio de mix?",
            new String[]{"3° a 6°", "2° a 5°", "1° a 4°", "-18° a -23°"}, 2),
        new Question("Quantidade de alface em cada lado do BigMac?",
            new String[]{"12g", "14g", "20g", "24g"}, 0),
        new Question("Quantas pedras de gelo vai no refrigerante pequena?",
            new String[]{"3", "15", "10", "5"}, 3),
        new Question("Quantas pedras de gelo vai no refrigerante média?",
            new String[]{"3", "15", "10", "5"}, 2),
        new Question("Quantas pedras de gelo vai no refrigerante grande?",
            new String[]{"3", "15", "10", "5"}, 1),
        new Question("Qual tempo de vida da batata na estufa em minutos?",
            new String[]{"7'", "8'", "9'", "6'"}, 0),
        new Question("Quantas tiros de cobertura vai no top sunday?",
            new String[]{"4", "3", "1", "2"}, 3),
        new Question("Quantas Oz de molho vai no Cheddar?",
            new String[]{"2 Oz", "1 Oz", "2/3 Oz", "1/3 Oz"}, 1)
    );
}
