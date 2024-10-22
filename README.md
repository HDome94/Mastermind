## Mastermind Spiel

Dieses Projekt ist eine Python-basierte Implementierung des beliebten Codeknack-Spiels Mastermind. Die Benutzeroberfläche wurde mit Tkinter erstellt.

## Funktionen
  - Einzelspieler-Modus: Spiele gegen den Computer und versuche, den geheimen Code zu erraten.
  - Mehrspieler-Modus: Unterstützt bis zu 5 Spieler.
  - Grafische Benutzeroberfläche: Eine intuitive Benutzeroberfläche, erstellt mit Tkinter, erlaubt es den Spielern, ihre Vermutungen abzugeben und den Spielverlauf zu verfolgen.
  - Zufällige Code-Generierung: Jeder Code wird zufällig aus 6 verschiedenen Farben ausgewählt.
  - Sprachunterstützung: Das Spiel unterstützt mehrere Sprachen (Deutsch, Englisch, Spanisch, Französisch, Italienisch, Chinesisch).

## Verwendete Technologien
  - Python: Die Hauptprogrammiersprache des Spiels.
  - Tkinter: Wird verwendet, um die grafische Benutzeroberfläche (GUI) zu erstellen.
  - gettext: Wird für die mehrsprachige Unterstützung verwendet.

## Spielregeln
  Ein geheimer Code bestehend aus 4 Farben wird zufällig generiert.
  Der/die Spieler müssen den Code erraten, indem sie die richtigen Farben in der richtigen Reihenfolge auswählen.
  
  Nach jeder Runde wird eine Rückmeldung gegeben:
    Richtige Farben: Anzahl der richtigen Farben an der richtigen Position.
    Farbe richtig, aber Position falsch: Anzahl der richtigen Farben an der falschen Position.
    
  Das Spiel endet, wenn der Code korrekt erraten wird oder eine festgelegte Anzahl von Runden vorbei ist.

## Spielstart:
  Starte die Datei gui.py, um das Spiel zu beginnen.
  Wähle die Anzahl der Spieler (1 bis 5).
  Gebe deine Vermutungen ab, indem du Farben auswählst und sie einreichst.
  Verfolge den Spielverlauf und die Rundenresultate in der grafischen Oberfläche.
