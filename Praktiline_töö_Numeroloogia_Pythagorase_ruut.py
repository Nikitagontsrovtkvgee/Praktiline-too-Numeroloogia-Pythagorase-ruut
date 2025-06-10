import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Цветовая схема
BG_COLOR = "#f5f5f5"  # Светло-серый фон
BUTTON_COLOR = "#4CAF50"  # Зеленый
TEXT_COLOR = "#333333"  # Темно-серый текст
ENTRY_COLOR = "#ffffff"  # Белый фон полей
FONT = ("Arial", 10)

# Характеристики чисел
iseloomustused = {
    '1': 'Tahtejõud ja enesekindlus.',
    '2': 'Energia ja tundlikkus.',
    '3': 'Loovus ja eneseväljendusoskus.',
    '4': 'Loogika ja püsivus.',
    '5': 'Intuitsioon ja kohanemisvõime.',
    '6': 'Vastutus ja hoolivus.',
    '7': 'Õnn ja sisemine talent.',
    '8': 'Organisatsioon ja tugevus.',
    '9': 'Intelligentsus ja mälu.',
}

def arvuta_tooarvud(sunnikuupaev):
    """Вычисляет все рабочие числа по дате рождения"""
    try:
        paev, kuu, aasta = map(int, sunnikuupaev.split('.'))
        esimene_rida = list(str(paev) + str(kuu) + str(aasta))

        tooarv1 = sum(map(int, list(str(paev) + str(kuu))))
        tooarv2 = sum(map(int, str(aasta)))
        tooarv3 = tooarv1 + tooarv2
        tooarv4 = sum(map(int, str(tooarv3)))
        tooarv5 = tooarv3 - 2 * int(str(paev)[0])
        tooarv6 = sum(map(int, str(abs(tooarv5))))

        teine_rida = list(str(tooarv3) + str(tooarv4) + str(tooarv5) + str(tooarv6))
        return ''.join(esimene_rida + teine_rida)
    except:
        return None

def loenda_numbrid(numbrijada):
    """Подсчитывает частоту встречаемости каждой цифры"""
    return {str(i): numbrijada.count(str(i)) for i in range(1, 10)}

def loo_ruut(loendur):
    """Создает квадрат Пифагора 3x3"""
    return [
        [loendur['1'] * '1', loendur['4'] * '4', loendur['7'] * '7'],
        [loendur['2'] * '2', loendur['5'] * '5', loendur['8'] * '8'],        
        [loendur['3'] * '3', loendur['6'] * '6', loendur['9'] * '9'],        
    ]

def saada_email(saaja, nimi, kuupaev, ruut, iseloom):
    """Отправляет результаты на email"""
    saatja = 'nikitosgoldboss@gmail.com'
    salasyna = 'pzvd agdo saxi ywtz'

    # Формируем содержимое письма
    sisu = f"<h2>Tere, {nimi}!</h2>"
    sisu += f"<p><b>Sünnikuupäev:</b> {kuupaev}</p>"
    sisu += "<h3>Pythagorase ruut:</h3><table border='1'>"
    
    for rida in ruut:
        sisu += "<tr><td>" + "</td><td>".join(rida) + "</td></tr>"
    
    sisu += "</table><h3>Iseloomustus:</h3><ul>"
    for nr, kirjeldus in iseloom.items():
        sisu += f"<li><b>{nr}:</b> {kirjeldus}</li>"
    sisu += "</ul>"

    # Создаем MIME сообщение
    msg = MIMEMultipart()
    msg['From'] = saatja
    msg['To'] = saaja
    msg['Subject'] = 'Sinu Pythagorase ruut'
    msg.attach(MIMEText(sisu, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(saatja, salasyna)
            server.send_message(msg)
        return True
    except Exception as e:
        print("Saatmise viga:", e)
        return False

def salvesta_faili(nimi, kuupaev, numbrid):
    """Сохраняет данные в файл"""
    with open("pythagorase_andmed.txt", "a", encoding="utf-8") as fail:
        fail.write(f"Nimi: {nimi}; Sünnipäev: {kuupaev}; Numbrid: {numbrid}\n")

def kaivita_rakendus():
    """Создает и запускает графический интерфейс"""
    aken = tk.Tk()
    aken.title("Pythagorase ruut")
    aken.geometry("600x500")
    aken.configure(bg=BG_COLOR)
    
    # Стиль для кнопок
    style = ttk.Style()
    style.configure('TButton', 
                    font=('Arial', 10, 'bold'), 
                    background=BUTTON_COLOR,
                    foreground='white',
                    padding=10,
                    borderwidth=0)
    
    style.map('TButton',
              background=[('active', '#45a049')],  # Темно-зеленый при наведении
              relief=[('pressed', 'sunken')])

    # Основной фрейм
    main_frame = ttk.Frame(aken, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Поля ввода
    ttk.Label(main_frame, text="Nimi:", background=BG_COLOR, font=FONT).grid(row=0, column=0, sticky=tk.W, pady=5)
    sisend_nimi = ttk.Entry(main_frame, width=30, font=FONT)
    sisend_nimi.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
    
    ttk.Label(main_frame, text="Sünnikuupäev (PP.KK.AAAA):", background=BG_COLOR, font=FONT).grid(row=1, column=0, sticky=tk.W, pady=5)
    sisend_kuupaev = ttk.Entry(main_frame, width=30, font=FONT)
    sisend_kuupaev.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
    
    ttk.Label(main_frame, text="E-mail:", background=BG_COLOR, font=FONT).grid(row=2, column=0, sticky=tk.W, pady=5)
    sisend_email = ttk.Entry(main_frame, width=30, font=FONT)
    sisend_email.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
    
    # Кнопка расчета
    arvuta_btn = ttk.Button(main_frame, 
                           text="Arvuta ja saada", 
                           style='TButton',
                           command=lambda: arvuta_nupp(sisend_nimi, sisend_kuupaev, sisend_email, tekstilahter))
    arvuta_btn.grid(row=3, column=0, columnspan=2, pady=15, ipadx=10, ipady=5)
    
    # Текстовое поле для результатов
    tekstilahter = tk.Text(main_frame, 
                          width=50, 
                          height=15, 
                          bg=ENTRY_COLOR, 
                          fg=TEXT_COLOR, 
                          font=FONT, 
                          wrap=tk.WORD,
                          padx=5,
                          pady=5)
    tekstilahter.grid(row=4, column=0, columnspan=2, pady=10, sticky=tk.NSEW)
    
    # Добавляем скроллбар
    scrollbar = ttk.Scrollbar(main_frame, command=tekstilahter.yview)
    scrollbar.grid(row=4, column=2, sticky='ns')
    tekstilahter['yscrollcommand'] = scrollbar.set
    
    # Настройка растягивания
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(4, weight=1)
    
    aken.mainloop()

def arvuta_nupp(nimi_entry, kuupaev_entry, email_entry, text_widget):
    """Обработчик нажатия кнопки"""
    nimi = nimi_entry.get()
    kuupaev = kuupaev_entry.get()
    email = email_entry.get()
    
    # Валидация даты
    try:
        datetime.strptime(kuupaev, "%d.%m.%Y")
    except ValueError:
        messagebox.showerror("Viga", "Palun sisesta kuupäev õiges formaadis (PP.KK.AAAA)")
        return
    
    # Вычисления
    numbrid = arvuta_tooarvud(kuupaev)
    if not numbrid:
        messagebox.showerror("Viga", "Vigane kuupäev!")
        return
    
    kordused = loenda_numbrid(numbrid)
    ruut = loo_ruut(kordused)
    
    # Вывод результатов
    text_widget.delete('1.0', tk.END)
    text_widget.insert(tk.END, "Pythagorase ruut:\n\n")
    
    for rida in ruut:
        text_widget.insert(tk.END, ' | '.join(rida) + '\n')
    
    text_widget.insert(tk.END, "\nIseloomustus:\n\n")
    iseloomustus = {nr: iseloomustused[nr] for nr in kordused if kordused[nr] > 0}
    for nr, kirjeldus in iseloomustus.items():
        text_widget.insert(tk.END, f"{nr}: {kirjeldus}\n")
    
    # Сохранение и отправка
    salvesta_faili(nimi, kuupaev, numbrid)
    
    if saada_email(email, nimi, kuupaev, ruut, iseloomustus):
        messagebox.showinfo("Edu", "Tulemused saadeti edukalt e-mailile!")
    else:
        messagebox.showerror("Viga", "E-maili saatmine ebaõnnestus. Palun kontrolli e-maili aadressi.")

if __name__ == "__main__":
    kaivita_rakendus()
