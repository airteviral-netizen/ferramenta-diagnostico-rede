import socket #servirá para pegar o nome do computador e o IP local.
import subprocess # servirá para rodar o comando ping do Windows.
import threading # servirá para rodar o ping em uma thread separada, evitando que a interface trave.
import customtkinter as ctk# servirá para criar a interface gráfica do programa.
import psutil # servirá para pegar o nome da placa de rede ativa.

#serve para deixar mais apresentável a interface do programa.
ctk.set_appearance_mode("System") # significa que a interface vai seguir o tema do sistema operacional (claro ou escuro).
ctk.set_default_color_theme("blue") # significa que a cor padrão da interface vai ser azul.

#essa é a base da nossa aplicação.
class FerramentaDiagnostico(ctk.CTk):

  def __init__(self):
    super().__init__()

    # Aqui conseguimos colocar o título da janela, o tamanho inicial e se ela pode ser redimensionada ou não.
    self.title("Ferramenta de Diagnóstico de Rede")
    self.geometry("750x600")
    self.resizable(True, True) # se mudar para False, False a janela não pode ser redimensionada. 
    #o que significa true, true é que a janela pode ser redimensionada tanto na horizontal quanto na vertical.
    #o que significa false, false é que a janela não pode ser redimensionada nem na horizontal nem na vertical.

    # Aqui chamamos a função que pega as informações do pc 
  
    self.montar_tela() # chama a função que monta a tela da aplicação.
    self.pegar_infos_pc() # chama a função que pega as informações do pc.

  def montar_tela(self):
    # Título principal do topo.
    lbl_titulo = ctk.CTkLabel( 
        self, text='''Diagnóstico de Rede
LUCAS -  DEODENIZ''', font=("Arial", 22, "bold")
    )
    lbl_titulo.pack(pady=15) #isso significa que o título vai ter um espaçamento de 15 pixels em cima e embaixo. 
    # e a função pack() serve para colocar o título na tela, e o parâmetro pady significa que vai ter um espaçamento de 15 pixels em cima e embaixo do título.

    # Informações do Computador
    frame_info = ctk.CTkFrame(self) # o CTK Significa Custom Tkinter, que é uma biblioteca que serve para criar interfaces gráficas mais bonitas e modernas do que o Tkinter padrão.
    frame_info.pack(fill="x", padx=20, pady=10)

    lbl_info_titulo = ctk.CTkLabel(
        frame_info, text="Informações da Minha Máquina", font=("Arial", 14, "bold")
    )
    lbl_info_titulo.pack(anchor="w", padx=10, pady=5)

    # Aqui serve para mostrar as informações do computador, como nome do PC, IP local e nome da placa de rede ativa.
    self.lbl_detalhes = ctk.CTkLabel(
        frame_info, text="Buscando informações...", justify="left", font=("Consolas", 12)
    )
    self.lbl_detalhes.pack(anchor="w", padx=10, pady=5)
    #O ctk label é um widget que serve para mostrar texto na tela, e o parâmetro justify significa que o 
    #texto vai ficar alinhado à esquerda, e o parâmetro font significa que a fonte do texto vai ser Consolas, tamanho 12.

    # Teste de Ping
    frame_ping = ctk.CTkFrame(self)
    frame_ping.pack(fill="x", padx=20, pady=10)

    lbl_ping_titulo = ctk.CTkLabel(
        frame_ping, text="Testar Conexão (Ping)", font=("Arial", 14, "bold")
    )
    lbl_ping_titulo.pack(anchor="w", padx=10, pady=5)

    # Caixa onde o usuário digita o site ou IP
    self.entrada_ip = ctk.CTkEntry(
        frame_ping, placeholder_text="Ex: google.com ou 8.8.8.8", width=350
    )
    self.entrada_ip.pack(side="left", padx=10, pady=10)

    # Botão que roda o ping
    btn_ping = ctk.CTkButton(
        frame_ping, text="Executar Ping", command=self.clique_botao_ping
    )
    btn_ping.pack(side="left", padx=5, pady=10)

    # Resultados 
    frame_res = ctk.CTkFrame(self)
    frame_res.pack(fill="both", expand=True, padx=20, pady=10)

    lbl_res_titulo = ctk.CTkLabel(
        frame_res, text="Resultados do Teste:", font=("Arial", 14, "bold")
    )
    lbl_res_titulo.pack(anchor="w", padx=10, pady=5)

    # Caixa de texto onde sai o resultado
    self.caixa_texto = ctk.CTkTextbox(frame_res, font=("Consolas", 12))
    self.caixa_texto.pack(fill="both", expand=True, padx=10, pady=5)

    # Botão para limpar a tela de resultados
    btn_limpar = ctk.CTkButton(
        self, text="Limpar Tela", fg_color="gray", command=self.limpar_tudo
    )
    btn_limpar.pack(pady=10)

  def pegar_infos_pc(self):
    # Aqui a gente descobre o nome do PC e o IP local de um jeito bem simples
    try:
      nome_computador = socket.gethostname()
      meu_ip = socket.gethostbyname(nome_computador)

      # Acha o nome da placa de rede ativa
      nome_rede = "Conexão Local"
      for placa, dados in psutil.net_if_stats().items():
        if dados.isup and placa != "Loopback Pseudo-Interface 1":
          nome_rede = placa
          break

      # Junta tudo num texto bonitinho para mostrar na tela
      texto_final = (
          f"• Nome do PC: {nome_computador}\n"
          f"• Meu IP Local: {meu_ip}\n"
          f"• Placa de Rede: {nome_rede}"
      )
      self.lbl_detalhes.configure(text=texto_final)

    except Exception as erro:
      self.lbl_detalhes.configure(text=f"Não consegui pegar os dados: {erro}")

  def clique_botao_ping(self):
    # Pega o que o usuário digitou na caixinha
    destino = self.entrada_ip.get().strip()

    if not destino:
      self.caixa_texto.insert("end", "⚠️ Eita! Digite um IP ou site válido antes.\n")
      return

    self.caixa_texto.insert("end", f"Testando a conexão com: {destino}...\n")

    # Usando thread para a tela não travar enquanto o ping roda
    processo_thread = threading.Thread(
        target=self.rodar_comando_ping, args=(destino,)
    )
    processo_thread.start()

  def rodar_comando_ping(self, destino):
    try:
      # Roda o comando ping do próprio Windows (4 disparos)
      comando = ["ping", "-n", "4", destino]
      resultado = subprocess.run(
          comando, capture_output=True, text=True, timeout=10
      )

      # Mostra se deu certo ou errado na caixinha de texto
      if resultado.returncode == 0:
        texto = f"\n[SUCESSO] O destino respondeu:\n{resultado.stdout}\n"
      else:
        texto = f"\n[FALHA] O destino não respondeu ou não existe:\n{resultado.stdout}\n"

      self.caixa_texto.insert("end", texto)
      self.caixa_texto.see("end")  # Joga a barra de rolagem para o final

    except Exception as erro:
      self.caixa_texto.insert(
          "end", f"\n[ERRO] Aconteceu um problema no teste: {erro}\n"
      )

  def limpar_tudo(self):
    # Limpa o que está escrito na caixa de resultados
    self.caixa_texto.delete("1.0", "end")


if __name__ == "__main__":
  
  app = FerramentaDiagnostico()
  app.mainloop()