// ---------------------------------------------
// IMPORTS E DEFINIÇÕES DE CLASSE
// ---------------------------------------------
package quiz.ui;

import quiz.core.QuizCore;
import quiz.questions.QuizQuestions;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Random;

public class QuizUI extends JFrame {
    // ---------------------------------------------
    // VARIÁVEIS PRINCIPAIS DO QUIZ
    // ---------------------------------------------
    private List<QuizCore.Question> questions = QuizQuestions.questions;
    private List<Integer> ordemPerguntas;
    private int rodada, score, acertos, tempoRestante;
    private javax.swing.Timer timer;
    private QuizCore.Question perguntaAtual;
    private List<Integer> ordemOpcoes;
    private int correctIndexEmbaralhado;

    // ---------------------------------------------
    // COMPONENTES DE INTERFACE
    // ---------------------------------------------
    // Labels, botões e painéis principais
    private JLabel lblPergunta, lblTimer, lblScore, lblContador, lblFeedback;
    private JButton[] btnOpcoes = new JButton[4];
    private JProgressBar progressBar;
    private JPanel painelOpcoes, painelQuiz, painelInicio, painelResultado;
    private JButton btnStart, btnRestart;
    private JLabel lblFinalScore, lblAcertos, lblMensagem;

    // Cores do estilo Kahoot
    private Color[] kahootColors = {
        new Color(255, 87, 34),    // Laranja vibrante
        new Color(0, 188, 212),    // Azul piscina
        new Color(255, 235, 59),   // Amarelo claro
        new Color(156, 39, 176)    // Roxo vibrante
    };
    private Color[] kahootTextColors = {
        Color.WHITE, Color.WHITE, new Color(255, 87, 34), Color.WHITE
    };

    // ---------------------------------------------
    // COMPONENTES DE FEEDBACK E MODAL
    // ---------------------------------------------
    private JPanel feedbackModal;
    private JLabel feedbackIcon, feedbackMsg;
    private Timer feedbackTimer;
    private JLayeredPane layeredPane;

    // ---------------------------------------------
    // CONSTRUTOR: MONTA TODA A INTERFACE E EVENTOS
    // ---------------------------------------------
    public QuizUI() {
        // Configuração da janela principal
        setTitle("Quiz McDonald's");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setExtendedState(JFrame.MAXIMIZED_BOTH); // Maximiza a janela
        setUndecorated(true); // Remove bordas e barra de título para tela cheia
        setResizable(false);
        getContentPane().setBackground(new Color(255, 235, 59));

        // -------------------
        // TELA DE INÍCIO
        // -------------------
        painelInicio = new JPanel();
        painelInicio.setLayout(new BoxLayout(painelInicio, BoxLayout.Y_AXIS));
        painelInicio.setBackground(new Color(255, 235, 59));
        JLabel lblTitulo = new JLabel("QUIZ McDonald's");
        lblTitulo.setFont(new Font("Arial", Font.BOLD, 36));
        lblTitulo.setForeground(new Color(211, 47, 47));
        lblTitulo.setAlignmentX(Component.CENTER_ALIGNMENT);
        painelInicio.add(Box.createVerticalGlue());
        painelInicio.add(lblTitulo);
        painelInicio.add(Box.createRigidArea(new Dimension(0, 30)));
        btnStart = new JButton("VAMOS JOGAR!");
        btnStart.setFont(new Font("Arial", Font.BOLD, 24));
        btnStart.setBackground(new Color(211, 47, 47));
        btnStart.setForeground(Color.WHITE);
        btnStart.setFocusPainted(false);
        btnStart.setAlignmentX(Component.CENTER_ALIGNMENT);
        painelInicio.add(btnStart);
        painelInicio.add(Box.createVerticalGlue());

        // -------------------
        // PAINEL PRINCIPAL DO QUIZ
        // -------------------
        painelQuiz = new JPanel(new BorderLayout(10, 10)) {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                Graphics2D g2d = (Graphics2D) g;
                GradientPaint gp = new GradientPaint(0, 0, new Color(255, 255, 255), getWidth(), getHeight(), new Color(255, 235, 59));
                g2d.setPaint(gp);
                g2d.fillRect(0, 0, getWidth(), getHeight());
            }
        };
        painelQuiz.setOpaque(false);
        painelQuiz.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(new Color(255, 87, 34), 3, true),
            BorderFactory.createEmptyBorder(32, 24, 32, 24)
        ));
        // TOPO: Info, timer, score
        JPanel painelTopo = new JPanel(new BorderLayout());
        painelTopo.setOpaque(false);
        JPanel painelInfo = new JPanel(new GridLayout(1, 4, 10, 10));
        painelInfo.setOpaque(false);
        lblContador = new JLabel("Pergunta 1/10", SwingConstants.CENTER);
        lblContador.setFont(new Font("Montserrat", Font.BOLD, 22));
        lblContador.setForeground(new Color(255, 87, 34));
        lblScore = new JLabel("Pontos: 0", SwingConstants.CENTER);
        lblScore.setFont(new Font("Montserrat", Font.BOLD, 32));
        lblScore.setForeground(new Color(0, 188, 212));
        lblScore.setBackground(new Color(255, 235, 59));
        lblScore.setOpaque(true);
        lblScore.setBorder(BorderFactory.createEmptyBorder(8, 16, 8, 16));
        lblTimer = new JLabel("Tempo: 10", SwingConstants.CENTER);
        lblTimer.setFont(new Font("Montserrat", Font.BOLD, 22));
        lblTimer.setForeground(new Color(156, 39, 176));
        progressBar = new JProgressBar(0, 10);
        progressBar.setValue(10);
        progressBar.setForeground(new Color(255, 87, 34));
        progressBar.setBackground(new Color(255, 241, 118));
        progressBar.setPreferredSize(new Dimension(400, 20));
        progressBar.setBorder(BorderFactory.createLineBorder(new Color(0, 188, 212), 2, true));
        painelInfo.add(lblContador);
        painelInfo.add(lblScore);
        painelInfo.add(lblTimer);
        painelInfo.add(progressBar);
        painelTopo.add(painelInfo, BorderLayout.NORTH);
        lblPergunta = new JLabel("Pergunta", SwingConstants.CENTER);
        lblPergunta.setFont(new Font("Montserrat", Font.BOLD, 32));
        lblPergunta.setForeground(new Color(0, 188, 212));
        lblPergunta.setBorder(BorderFactory.createEmptyBorder(24, 0, 24, 0));
        painelTopo.add(lblPergunta, BorderLayout.SOUTH);

        // OPÇÕES (botões)
        painelOpcoes = new JPanel(new GridLayout(2, 2, 32, 32));
        painelOpcoes.setOpaque(false);
        painelOpcoes.removeAll();
        // Inicializa apenas os botões, sem listeners ou textos ainda
        for (int i = 0; i < 4; i++) {
            btnOpcoes[i] = new JButton();
            btnOpcoes[i].setFont(new Font("Montserrat", Font.BOLD, 26));
            btnOpcoes[i].setBackground(kahootColors[i]);
            btnOpcoes[i].setForeground(kahootTextColors[i]);
            btnOpcoes[i].setFocusPainted(false);
            btnOpcoes[i].setBorder(BorderFactory.createLineBorder(Color.WHITE, 5, true));
            btnOpcoes[i].setPreferredSize(new Dimension(260, 80));
            btnOpcoes[i].setCursor(new Cursor(Cursor.HAND_CURSOR));
            painelOpcoes.add(btnOpcoes[i]);
        }
        painelOpcoes.revalidate();
        painelOpcoes.repaint();

        // FEEDBACK (não mais usado, mas mantido para compatibilidade)
        lblFeedback = new JLabel("", SwingConstants.CENTER);
        lblFeedback.setFont(new Font("Montserrat", Font.BOLD, 38));
        lblFeedback.setOpaque(true);
        lblFeedback.setVisible(false);
        lblFeedback.setBorder(BorderFactory.createLineBorder(Color.LIGHT_GRAY, 3, true));
        lblFeedback.setBackground(new Color(255,255,255,230));

        painelQuiz.add(painelTopo, BorderLayout.NORTH);
        painelQuiz.add(painelOpcoes, BorderLayout.CENTER);
        painelQuiz.add(lblFeedback, BorderLayout.SOUTH);
        painelQuiz.setComponentZOrder(lblFeedback, 0); // Garante que feedback fique acima
        painelQuiz.setComponentZOrder(painelOpcoes, 1); // Garante que opções fiquem visíveis

        // -------------------
        // PAINEL DE RESULTADO FINAL
        // -------------------
        painelResultado = new JPanel() {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                Graphics2D g2d = (Graphics2D) g;
                GradientPaint gp = new GradientPaint(0, 0, new Color(255, 255, 255), getWidth(), getHeight(), new Color(156, 39, 176));
                g2d.setPaint(gp);
                g2d.fillRect(0, 0, getWidth(), getHeight());
            }
        };
        painelResultado.setOpaque(false);
        painelResultado.setLayout(new BoxLayout(painelResultado, BoxLayout.Y_AXIS));
        JLabel lblRes = new JLabel("RESULTADO FINAL");
        lblRes.setFont(new Font("Arial", Font.BOLD, 32));
        lblRes.setForeground(new Color(211, 47, 47));
        lblRes.setAlignmentX(Component.CENTER_ALIGNMENT);
        lblFinalScore = new JLabel();
        lblFinalScore.setFont(new Font("Arial", Font.BOLD, 28));
        lblFinalScore.setForeground(new Color(255, 193, 7));
        lblFinalScore.setAlignmentX(Component.CENTER_ALIGNMENT);
        lblAcertos = new JLabel();
        lblAcertos.setFont(new Font("Arial", Font.BOLD, 22));
        lblAcertos.setForeground(Color.DARK_GRAY);
        lblAcertos.setAlignmentX(Component.CENTER_ALIGNMENT);
        lblMensagem = new JLabel();
        lblMensagem.setFont(new Font("Arial", Font.BOLD, 22));
        lblMensagem.setForeground(new Color(211, 47, 47));
        lblMensagem.setAlignmentX(Component.CENTER_ALIGNMENT);
        btnRestart = new JButton("JOGAR NOVAMENTE");
        btnRestart.setFont(new Font("Arial", Font.BOLD, 22));
        btnRestart.setBackground(new Color(211, 47, 47));
        btnRestart.setForeground(Color.WHITE);
        btnRestart.setFocusPainted(false);
        btnRestart.setAlignmentX(Component.CENTER_ALIGNMENT);
        painelResultado.add(Box.createVerticalGlue());
        painelResultado.add(lblRes);
        painelResultado.add(Box.createRigidArea(new Dimension(0, 20)));
        painelResultado.add(lblFinalScore);
        painelResultado.add(lblAcertos);
        painelResultado.add(lblMensagem);
        painelResultado.add(Box.createRigidArea(new Dimension(0, 20)));
        painelResultado.add(btnRestart);
        painelResultado.add(Box.createVerticalGlue());

        // -------------------
        // LAYEREDPANE PARA MODAL DE FEEDBACK
        // -------------------
        layeredPane = new JLayeredPane();
        layeredPane.setLayout(null);
        layeredPane.setPreferredSize(new Dimension(1280, 720));
        painelQuiz.setBounds(0, 0, 1280, 720);
        layeredPane.add(painelQuiz, JLayeredPane.DEFAULT_LAYER);
        // Modal de feedback centralizado
        feedbackModal = new JPanel() {
            @Override
            protected void paintComponent(Graphics g) {
                Graphics2D g2 = (Graphics2D) g.create();
                // Sombra
                g2.setColor(new Color(0,0,0,40));
                g2.fillRoundRect(8, 8, getWidth()-16, getHeight()-16, 32, 32);
                // Fundo
                g2.setColor(getBackground());
                g2.fillRoundRect(0, 0, getWidth()-8, getHeight()-8, 28, 28);
                g2.dispose();
                super.paintComponent(g);
            }
        };
        feedbackModal.setLayout(new BoxLayout(feedbackModal, BoxLayout.Y_AXIS));
        feedbackModal.setOpaque(true);
        feedbackModal.setBackground(new Color(255,255,255,240));
        feedbackModal.setBorder(BorderFactory.createLineBorder(Color.LIGHT_GRAY, 6, true));
        feedbackIcon = new JLabel("", SwingConstants.CENTER);
        feedbackIcon.setFont(new Font("Arial", Font.BOLD, 64));
        feedbackIcon.setAlignmentX(Component.CENTER_ALIGNMENT);
        feedbackMsg = new JLabel("", SwingConstants.CENTER);
        feedbackMsg.setFont(new Font("Montserrat", Font.BOLD, 36));
        feedbackMsg.setAlignmentX(Component.CENTER_ALIGNMENT);
        feedbackModal.add(Box.createVerticalGlue());
        feedbackModal.add(feedbackIcon);
        feedbackModal.add(Box.createRigidArea(new Dimension(0, 16)));
        feedbackModal.add(feedbackMsg);
        feedbackModal.add(Box.createVerticalGlue());
        feedbackModal.setVisible(false);
        // Responsividade: tamanho proporcional à janela
        int modalW = Math.max(320, Math.min( (int)(getWidth()*0.4), 700));
        int modalH = Math.max(160, Math.min( (int)(getHeight()*0.22), 350));
        feedbackModal.setSize(modalW, modalH);
        layeredPane.add(feedbackModal, JLayeredPane.POPUP_LAYER);
        // Centraliza modal ao redimensionar e ajusta tamanho/fonte
        layeredPane.addComponentListener(new ComponentAdapter() {
            public void componentResized(ComponentEvent e) {
                painelQuiz.setBounds(0, 0, layeredPane.getWidth(), layeredPane.getHeight());
                int modalW = Math.max(320, Math.min( (int)(layeredPane.getWidth()*0.4), 700));
                int modalH = Math.max(160, Math.min( (int)(layeredPane.getHeight()*0.22), 350));
                feedbackModal.setSize(modalW, modalH);
                feedbackModal.setLocation((layeredPane.getWidth()-modalW)/2, (layeredPane.getHeight()-modalH)/2);
                // Ajusta fonte conforme tamanho
                int iconFont = Math.max(32, modalH/3);
                int msgFont = Math.max(18, modalH/6);
                feedbackIcon.setFont(new Font("Arial", Font.BOLD, iconFont));
                feedbackMsg.setFont(new Font("Montserrat", Font.BOLD, msgFont));
            }
        });

        // -------------------
        // EVENTOS DE BOTÕES E INICIALIZAÇÃO
        // -------------------
        setContentPane(painelInicio);
        btnStart.addActionListener(e -> iniciarQuiz());
        btnRestart.addActionListener(e -> iniciarQuiz());
        setVisible(true);

        // Barra superior minimalista com botões de controle (estilo navegador)
        JPanel barraSuperior = new JPanel(null) {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                Graphics2D g2 = (Graphics2D) g;
                g2.setColor(new Color(245,245,245,220));
                g2.fillRoundRect(0, 0, getWidth(), getHeight(), 18, 18);
            }
        };
        barraSuperior.setBounds(0, 0, getWidth(), 36);
        barraSuperior.setOpaque(false);
        // Botão minimizar
        JButton btnMin = new JButton("–");
        btnMin.setFont(new Font("Arial", Font.BOLD, 18));
        btnMin.setBackground(new Color(245,245,245,0));
        btnMin.setForeground(new Color(80,80,80));
        btnMin.setFocusPainted(false);
        btnMin.setBorder(BorderFactory.createEmptyBorder(0, 0, 0, 0));
        btnMin.setBounds(getWidth()-120, 4, 28, 28);
        btnMin.setCursor(new Cursor(Cursor.HAND_CURSOR));
        btnMin.addActionListener(e -> setState(Frame.ICONIFIED));
        // Botão maximizar/restaurar
        JButton btnMax = new JButton("❐");
        btnMax.setFont(new Font("Arial", Font.BOLD, 16));
        btnMax.setBackground(new Color(245,245,245,0));
        btnMax.setForeground(new Color(80,80,80));
        btnMax.setFocusPainted(false);
        btnMax.setBorder(BorderFactory.createEmptyBorder(0, 0, 0, 0));
        btnMax.setBounds(getWidth()-86, 4, 28, 28);
        btnMax.setCursor(new Cursor(Cursor.HAND_CURSOR));
        btnMax.addActionListener(e -> {
            if (getExtendedState() == JFrame.MAXIMIZED_BOTH) {
                setExtendedState(JFrame.NORMAL);
                setUndecorated(false);
                setResizable(true);
            } else {
                setExtendedState(JFrame.MAXIMIZED_BOTH);
                setUndecorated(true);
                setResizable(false);
            }
        });
        // Botão fechar
        JButton btnFechar = new JButton("✕");
        btnFechar.setFont(new Font("Arial", Font.BOLD, 18));
        btnFechar.setBackground(new Color(245,245,245,0));
        btnFechar.setForeground(new Color(211,47,47));
        btnFechar.setFocusPainted(false);
        btnFechar.setBorder(BorderFactory.createEmptyBorder(0, 0, 0, 0));
        btnFechar.setBounds(getWidth()-44, 4, 36, 28); // Ajusta largura e posição para o extremo direito
        btnFechar.setCursor(new Cursor(Cursor.HAND_CURSOR));
        btnFechar.addActionListener(e -> System.exit(0));
        // Hover para destaque
        btnFechar.addMouseListener(new MouseAdapter() {
            public void mouseEntered(MouseEvent e) {
                btnFechar.setBackground(new Color(211,47,47,40));
                btnFechar.setForeground(Color.WHITE);
            }
            public void mouseExited(MouseEvent e) {
                btnFechar.setBackground(new Color(245,245,245,0));
                btnFechar.setForeground(new Color(211,47,47));
            }
        });
        // Adiciona tooltips aos botões de controle para acessibilidade
        btnMin.setToolTipText("Minimizar janela");
        btnMax.setToolTipText("Maximizar/Restaurar janela");
        btnFechar.setToolTipText("Fechar o quiz");
        // Permite arrastar a janela quando não está em tela cheia
        barraSuperior.addMouseListener(new MouseAdapter() {
            public void mousePressed(MouseEvent e) { }
        });
        barraSuperior.addMouseMotionListener(new MouseMotionAdapter() {
            public void mouseDragged(MouseEvent e) {
                if (!isUndecorated()) {
                    Point p = e.getLocationOnScreen();
                    setLocation(p.x - e.getX(), p.y - e.getY());
                }
            }
        });
        barraSuperior.add(btnMin);
        barraSuperior.add(btnMax);
        barraSuperior.add(btnFechar);
        getLayeredPane().add(barraSuperior, JLayeredPane.POPUP_LAYER);
        barraSuperior.setVisible(true);
        addComponentListener(new ComponentAdapter() {
            public void componentResized(ComponentEvent e) {
                barraSuperior.setBounds(0, 0, getWidth(), 36);
                btnMin.setBounds(getWidth()-120, 4, 28, 28);
                btnMax.setBounds(getWidth()-86, 4, 28, 28);
                btnFechar.setBounds(getWidth()-44, 4, 36, 28); // Mantém no canto direito
            }
        });
    }

    // ---------------------------------------------
    // MÉTODO PRINCIPAL
    // ---------------------------------------------
    public static void main(String[] args) {
        SwingUtilities.invokeLater(QuizUI::new);
    }

    // ---------------------------------------------
    // INICIALIZAÇÃO E FLUXO DO QUIZ
    // ---------------------------------------------
    private void iniciarQuiz() {
        rodada = 0;
        score = 0;
        acertos = 0;
        ordemPerguntas = new ArrayList<>();
        for (int i = 0; i < questions.size(); i++) ordemPerguntas.add(i);
        Collections.shuffle(ordemPerguntas);
        setContentPane(layeredPane);
        layeredPane.setSize(getWidth(), getHeight());
        layeredPane.setPreferredSize(new Dimension(getWidth(), getHeight()));
        painelQuiz.setBounds(0, 0, layeredPane.getWidth(), layeredPane.getHeight());
        feedbackModal.setLocation((layeredPane.getWidth()-600)/2, (layeredPane.getHeight()-260)/2);
        revalidate();
        proximaPergunta();
    }

    // ---------------------------------------------
    // LÓGICA DE CADA PERGUNTA
    // ---------------------------------------------
    private boolean respondido = false; // Garante resposta única por pergunta
    private void proximaPergunta() {
        respondido = false; // Reset para nova pergunta
        if (rodada >= 10) {
            mostrarResultado();
            return;
        }
        int idx = ordemPerguntas.get(rodada);
        perguntaAtual = questions.get(idx);
        ordemOpcoes = new ArrayList<>(Arrays.asList(0,1,2,3));
        Collections.shuffle(ordemOpcoes);
        lblPergunta.setText("<html><div style='text-align:center; font-size:28px; font-weight:bold; color:#1976d2; margin-top:32px; margin-bottom:32px;'>" + perguntaAtual.question + "</div></html>");
        painelOpcoes.removeAll();
        for (int i = 0; i < 4; i++) {
            btnOpcoes[i].setText(perguntaAtual.options[ordemOpcoes.get(i)]);
            btnOpcoes[i].setEnabled(true);
            btnOpcoes[i].setBackground(kahootColors[i]);
            btnOpcoes[i].setForeground(kahootTextColors[i]);
            btnOpcoes[i].setBorder(BorderFactory.createLineBorder(Color.WHITE, 5, true));
            // Remove todos os ActionListeners antigos para evitar múltiplas chamadas
            for (ActionListener al : btnOpcoes[i].getActionListeners()) {
                btnOpcoes[i].removeActionListener(al);
            }
            final int idxBtn = i;
            btnOpcoes[i].addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    responder(ordemOpcoes.get(idxBtn));
                }
            });
            // Remove todos os MouseListeners antigos para evitar duplicidade
            for (MouseListener ml : btnOpcoes[i].getMouseListeners()) {
                btnOpcoes[i].removeMouseListener(ml);
            }
            btnOpcoes[i].addMouseListener(new java.awt.event.MouseAdapter() {
                public void mouseEntered(java.awt.event.MouseEvent evt) {
                    btnOpcoes[idxBtn].setBackground(new Color(255, 255, 255));
                    btnOpcoes[idxBtn].setForeground(kahootColors[idxBtn]);
                }
                public void mouseExited(java.awt.event.MouseEvent evt) {
                    btnOpcoes[idxBtn].setBackground(kahootColors[idxBtn]);
                    btnOpcoes[idxBtn].setForeground(kahootTextColors[idxBtn]);
                }
            });
            painelOpcoes.add(btnOpcoes[i]);
        }
        painelOpcoes.revalidate();
        painelOpcoes.repaint();
        lblContador.setText("Pergunta " + (rodada+1) + "/10");
        lblScore.setText("Pontos: " + score);
        tempoRestante = 10;
        lblTimer.setText("Tempo: " + tempoRestante);
        progressBar.setMaximum(10);
        progressBar.setValue(10);
        lblFeedback.setVisible(false);
        if (timer != null) timer.stop();
        timer = new javax.swing.Timer(1000, new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                tempoRestante--;
                lblTimer.setText("Tempo: " + tempoRestante);
                progressBar.setValue(tempoRestante);
                if (tempoRestante <= 0) {
                    timer.stop();
                    responder(-1); // tempo esgotado
                }
            }
        });
        timer.setInitialDelay(0);
        timer.start();
    }

    // ---------------------------------------------
    // FEEDBACK MODAL (ACERTO/ERRO/TEMPO ESGOTADO)
    // ---------------------------------------------
    private void mostrarFeedbackModal(String tipo, String mensagem) {
        Color cor;
        String icone;
        String frase = mensagem;
        if ("acerto".equals(tipo)) {
            cor = new Color(0, 230, 118);
            icone = "\u2714"; // check
            // Seleciona frase aleatória de acerto
            String[] frases = QuizCore.frasesAcerto;
            frase = frases[new java.util.Random().nextInt(frases.length)];
        } else if ("erro".equals(tipo)) {
            cor = new Color(255, 87, 34);
            icone = "\u2716"; // X
            // Seleciona frase aleatória de erro
            String[] frases = QuizCore.frasesErro;
            frase = frases[new java.util.Random().nextInt(frases.length)];
        } else {
            cor = new Color(255, 205, 210);
            icone = "\u23F1"; // relógio
            // Mantém mensagem padrão de tempo esgotado
        }
        feedbackModal.setBackground(new Color(cor.getRed(), cor.getGreen(), cor.getBlue(), 240));
        feedbackIcon.setText(icone);
        feedbackIcon.setForeground(Color.WHITE);
        feedbackMsg.setText(frase);
        feedbackMsg.setForeground(Color.WHITE);
        // Garante que o modal está no topo e centralizado
        if (feedbackModal.getParent() != layeredPane) {
            layeredPane.add(feedbackModal, JLayeredPane.DRAG_LAYER);
        } else {
            layeredPane.setLayer(feedbackModal, JLayeredPane.DRAG_LAYER);
        }
        // Responsividade: tamanho proporcional à janela
        int modalW = Math.max(320, Math.min( (int)(layeredPane.getWidth()*0.4), 700));
        int modalH = Math.max(160, Math.min( (int)(layeredPane.getHeight()*0.22), 350));
        feedbackModal.setSize(modalW, modalH);
        feedbackModal.setLocation((layeredPane.getWidth()-modalW)/2, (layeredPane.getHeight()-modalH)/2);
        // Ajusta fonte conforme tamanho
        int iconFont = Math.max(32, modalH/3);
        int msgFont = Math.max(18, modalH/6);
        feedbackIcon.setFont(new Font("Arial", Font.BOLD, iconFont));
        feedbackMsg.setFont(new Font("Montserrat", Font.BOLD, msgFont));
        feedbackModal.setVisible(true);
        feedbackModal.revalidate();
        feedbackModal.repaint();
        layeredPane.revalidate();
        layeredPane.repaint();
        // Bloqueia botões
        for (JButton btn : btnOpcoes) btn.setEnabled(false);
        if (feedbackTimer != null && feedbackTimer.isRunning()) feedbackTimer.stop();
        feedbackTimer = new Timer(2000, e -> {
            feedbackModal.setVisible(false);
            rodada++;
            proximaPergunta();
        });
        feedbackTimer.setRepeats(false);
        feedbackTimer.start();
    }

    // ---------------------------------------------
    // LÓGICA DE RESPOSTA DO USUÁRIO
    // ---------------------------------------------
    private void responder(int idxEscolhido) {
        if (respondido) return; // Bloqueia múltiplas respostas
        respondido = true;
        if (timer != null) timer.stop();
        boolean acertou = (idxEscolhido == correctIndexEmbaralhado); // Corrigido para usar o índice embaralhado
        int pontos = 0;
        String mensagem;
        String tipoFeedback;
        if (idxEscolhido == -1) {
            mensagem = "⏰ Que pena, seu tempo acabou!";
            tipoFeedback = "tempo";
            playSound("tempo");
        } else if (acertou) {
            acertos++;
            pontos = tempoRestante > 5 ? 100 : 50;
            score += pontos;
            mensagem = "✅ Acertou! +" + pontos + " pontos";
            tipoFeedback = "acerto";
            playSound("acerto");
            showConfetti();
        } else {
            mensagem = "❌ Errou! +0 pontos";
            tipoFeedback = "erro";
            playSound("erro");
        }
        lblScore.setText("Pontos: " + score);
        mostrarFeedbackModal(tipoFeedback, mensagem);
    }

    // ---------------------------------------------
    // SONS DE FEEDBACK
    // ---------------------------------------------
    private void playSound(String type) {
        // Sons simples usando beep do sistema
        if (type.equals("acerto")) {
            Toolkit.getDefaultToolkit().beep();
        } else if (type.equals("erro")) {
            for (int i = 0; i < 2; i++) {
                Toolkit.getDefaultToolkit().beep();
                try { Thread.sleep(100); } catch (InterruptedException e) {}
            }
        } else if (type.equals("tempo")) {
            for (int i = 0; i < 3; i++) {
                Toolkit.getDefaultToolkit().beep();
                try { Thread.sleep(60); } catch (InterruptedException e) {}
            }
        }
    }

    // ---------------------------------------------
    // ANIMAÇÃO DE CONFETTI (ACERTO)
    // ---------------------------------------------
    private JPanel confettiPanel;
    private void showConfetti() {
        if (confettiPanel != null) painelQuiz.remove(confettiPanel);
        confettiPanel = new JPanel() {
            java.util.List<Point> confetti = new ArrayList<>();
            Color[] confettiColors = {new Color(255,87,34), new Color(0,188,212), new Color(255,235,59), new Color(156,39,176), new Color(0,230,118), new Color(255,193,7)};
            { // Gera confetes
                Random r = new Random();
                for (int i = 0; i < 80; i++) confetti.add(new Point(r.nextInt(getWidth()), r.nextInt(getHeight())));
            }
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                Random r = new Random();
                for (Point p : confetti) {
                    g.setColor(confettiColors[r.nextInt(confettiColors.length)]);
                    g.fillOval(p.x, p.y, 10+r.nextInt(10), 10+r.nextInt(10));
                }
            }
        };
        confettiPanel.setOpaque(false);
        confettiPanel.setBounds(0,0,painelQuiz.getWidth(),painelQuiz.getHeight());
        painelQuiz.add(confettiPanel, Integer.valueOf(2));
        painelQuiz.repaint();
        new javax.swing.Timer(900, e -> { painelQuiz.remove(confettiPanel); painelQuiz.repaint(); }).start();
    }

    // ---------------------------------------------
    // TELA DE RESULTADO FINAL
    // ---------------------------------------------
    private void mostrarResultado() {
        setContentPane(painelResultado);
        lblFinalScore.setText("Sua pontuação final é: " + score + " pontos");
        lblAcertos.setText("Você acertou " + acertos + " de " + questions.size() + " perguntas");
        if (acertos == questions.size()) {
            lblMensagem.setText("PERFEITO! Você é um mestre do McDonald's! 🎉");
        } else if (acertos >= 8) {
            lblMensagem.setText("Excelente! Você sabe muito! 😃");
        } else if (acertos >= 5) {
            lblMensagem.setText("Muito bom! Continue praticando para ficar ainda melhor!");
        } else {
            lblMensagem.setText("Continue praticando! Você vai melhorar! 💪");
        }
        revalidate();
        repaint();
    }
}
