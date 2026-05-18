import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class SalaryApp:
    """Главный класс приложения - принцип инкапсуляции ООП"""
    
    def __init__(self, root):
        """Конструктор: инициализация интерфейса и переменных"""
        self.root = root
        self.root.title("Анализ медианной зарплаты - Вариант 8")
        self.root.geometry("1100x750")
        
        self.data = []          # Список для хранения загруженных данных
        self.current_fig = None # Текущий график для сохранения
        
        # СОЗДАНИЕ ИНТЕРФЕЙСА
        self._create_widgets()
    
    def _create_widgets(self):
        """Создание всех элементов интерфейса"""
        
        # Верхняя панель с кнопками
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=5)
        
        # Кнопка загрузки файла (вариант 8 - открытие файла с данными)
        tk.Button(top_frame, text="1. Загрузить CSV", command=self.load_data, 
                  bg="lightblue", width=15).pack(side=tk.LEFT, padx=5)
        
        # Кнопка расчёта процентов роста/падения
        tk.Button(top_frame, text="2. Рассчитать проценты", command=self.calc_percents, 
                  bg="lightgreen", width=15).pack(side=tk.LEFT, padx=5)
        
        # Поле для ввода периода скользящей средней (N)
        tk.Label(top_frame, text="Период N:").pack(side=tk.LEFT, padx=(20,2))
        self.n_entry = tk.Entry(top_frame, width=5)
        self.n_entry.insert(0, "3")
        self.n_entry.pack(side=tk.LEFT)
        
        # Поле для ввода количества лет прогноза (K)
        tk.Label(top_frame, text="Прогноз на K лет:").pack(side=tk.LEFT, padx=(10,2))
        self.k_entry = tk.Entry(top_frame, width=5)
        self.k_entry.insert(0, "5")
        self.k_entry.pack(side=tk.LEFT)
        
        # Кнопка построения прогноза
        tk.Button(top_frame, text="3. Прогноз", command=self.make_forecast, 
                  bg="lightcoral", width=10).pack(side=tk.LEFT, padx=5)
        
        # Кнопка сохранения графика (экспорт в PNG/SVG)
        tk.Button(top_frame, text="Сохранить график", command=self.save_plot, 
                  bg="lightyellow", width=12).pack(side=tk.LEFT, padx=5)
        
        # ТАБЛИЦА ДЛЯ ВЫВОДА ДАННЫХ
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Полоса прокрутки для таблицы
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(table_frame, columns=("year", "men", "women"), 
                                  show="headings", yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.tree.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Настройка заголовков таблицы
        self.tree.heading("year", text="Год")
        self.tree.heading("men", text="Мужчины (руб)")
        self.tree.heading("women", text="Женщины (руб)")
        
        # Настройка ширины колонок
        self.tree.column("year", width=80)
        self.tree.column("men", width=150)
        self.tree.column("women", width=150)
        
        # ОБЛАСТЬ ДЛЯ ГРАФИКА
        self.fig_frame = tk.Frame(self.root)
        self.fig_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Строка статуса
        self.status = tk.Label(self.root, text="Готов. Загрузите CSV файл.", fg="gray")
        self.status.pack(pady=5)
    
    def load_data(self):
        """Загрузка данных из CSV файла"""
        filename = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not filename:
            return
        
        try:
            # Очищаем таблицу
            for row in self.tree.get_children():
                self.tree.delete(row)
            
            self.data = []
            
            # Чтение CSV файла
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    year = int(row['year'])
                    men = float(row['men_salary'])
                    women = float(row['women_salary'])
                    self.data.append((year, men, women))
                    self.tree.insert("", tk.END, values=(year, f"{men:.0f}", f"{women:.0f}"))
            
            self.status.config(text=f"Загружено {len(self.data)} записей", fg="green")
            self.plot_data()  # Строим график после загрузки
            
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def plot_data(self, forecast_men=None, forecast_women=None, forecast_years=None):
        """Построение графика. Прогноз отображается пунктирной линией другого цвета"""
        if not self.data:
            return
        
        # Очищаем предыдущий график
        for widget in self.fig_frame.winfo_children():
            widget.destroy()
        
        # Подготовка данных
        years = [d[0] for d in self.data]
        men = [d[1] for d in self.data]
        women = [d[2] for d in self.data]
        
        # Создание графика
        self.current_fig, ax = plt.subplots(figsize=(10, 5))
        
        # Фактические данные (синий для мужчин, красный для женщин)
        ax.plot(years, men, 'b-o', label='Мужчины (факт)', linewidth=2, markersize=6)
        ax.plot(years, women, 'r-o', label='Женщины (факт)', linewidth=2, markersize=6)
        
        # Прогнозные данные (пунктирная линия - соответствует требованию "другим цветом")
        if forecast_men and forecast_women and forecast_years:
            ax.plot(forecast_years, forecast_men, 'b--s', label='Мужчины (прогноз)', linewidth=2, markersize=6)
            ax.plot(forecast_years, forecast_women, 'r--s', label='Женщины (прогноз)', linewidth=2, markersize=6)
        
        # Настройка графика
        ax.set_xlabel('Год', fontsize=12)
        ax.set_ylabel('Зарплата (руб)', fontsize=12)
        ax.set_title('Медианная зарплата в России', fontsize=14)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Встраивание графика в интерфейс
        canvas = FigureCanvasTkAgg(self.current_fig, self.fig_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Панель инструментов для интерактивного масштабирования
        toolbar = NavigationToolbar2Tk(canvas, self.fig_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def calc_percents(self):
        """Расчёт максимального и минимального процента роста/падения"""
        if len(self.data) < 2:
            messagebox.showwarning("Нет данных", "Сначала загрузите файл")
            return
        
        # Инициализация переменных
        max_m = min_m = max_w = min_w = 0
        y_max_m = y_min_m = y_max_w = y_min_w = 0
        
        # Проходим по всем годам, начиная со второго
        for i in range(1, len(self.data)):
            y, m_c, w_c = self.data[i]
            _, m_p, w_p = self.data[i-1]
            
            # Формула процента роста: (текущий - предыдущий) / предыдущий * 100
            gm = (m_c - m_p) / m_p * 100  # процент для мужчин
            gw = (w_c - w_p) / w_p * 100  # процент для женщин
            
            # Поиск максимумов и минимумов
            if gm > max_m: max_m, y_max_m = gm, y
            if gm < min_m: min_m, y_min_m = gm, y
            if gw > max_w: max_w, y_max_w = gw, y
            if gw < min_w: min_w, y_min_w = gw, y
        
        # Формирование сообщения с результатами
        msg = f"Мужчины:\n  Макс. рост: {max_m:.1f}% ({y_max_m} г.)\n  Мин. рост: {min_m:.1f}% ({y_min_m} г.)\n\n"
        msg += f"Женщины:\n  Макс. рост: {max_w:.1f}% ({y_max_w} г.)\n  Мин. рост: {min_w:.1f}% ({y_min_w} г.)"
        messagebox.showinfo("Результаты анализа", msg)
    
    def moving_average(self, values, n, k):
        """
        Метод скользящей средней (из методички стр. 3-4)
        values - исходный ряд данных
        n - период скользящей средней
        k - количество прогнозных значений
        """
        result = []
        last = values.copy()
        for _ in range(k):
            # Берём последние n значений и вычисляем среднее
            avg = sum(last[-n:]) / n
            result.append(avg)
            # Добавляем прогноз в конец для следующего шага
            last.append(avg)
        return result
    
    def make_forecast(self):
        """Построение прогноза методом скользящей средней"""
        if len(self.data) < 2:
            messagebox.showwarning("Нет данных", "Сначала загрузите файл")
            return
        
        # Получение параметров N и K от пользователя
        try:
            n = int(self.n_entry.get())
            k = int(self.k_entry.get())
            if n < 1 or k < 1:
                raise ValueError
        except:
            messagebox.showerror("Ошибка", "Введите положительные числа")
            return
        
        # Подготовка данных
        men = [d[1] for d in self.data]
        women = [d[2] for d in self.data]
        
        # Расчёт прогноза
        men_forecast = self.moving_average(men, n, k)
        women_forecast = self.moving_average(women, n, k)
        
        # Генерация годов для прогноза
        years = [d[0] for d in self.data]
        forecast_years = [years[-1] + i + 1 for i in range(k)]
        
        # Перерисовка графика с прогнозом
        self.plot_data(men_forecast, women_forecast, forecast_years)
        self.status.config(text=f"Прогноз построен: N={n}, прогноз на {k} лет", fg="blue")
    
    def save_plot(self):
        """Экспорт графика в файл (PNG или SVG)"""
        if not self.current_fig:
            messagebox.showwarning("Нет графика", "Сначала загрузите данные")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png", 
            filetypes=[("PNG", "*.png"), ("SVG", "*.svg")]
        )
        if filename:
            self.current_fig.savefig(filename, dpi=150)
            messagebox.showinfo("Успех", f"График сохранён")

# Точка входа в программу
if __name__ == "__main__":
    root = tk.Tk()
    app = SalaryApp(root)
    root.mainloop()
