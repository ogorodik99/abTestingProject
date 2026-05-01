import sys
import os
# Добавляем корень проекта в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Scripts import gui, data_manager, analysis, reports
from Scripts.config import CFG

def handle_import():
    csv_path = os.path.join(CFG['data_dir'], "ab_data.csv")
    data_manager.normalize_data(csv_path, CFG['data_dir'])
    print("Данные импортированы")

def handle_analysis():
    u, e = data_manager.load_data(CFG['data_dir'])
    res = analysis.calculate_ctr_stats(u, e)
    reports.create_plots(u, e, CFG['graphics_dir'])
    print(res)

if __name__ == "__main__":
    app = gui.create_main_window(handle_import, handle_analysis)
    app.mainloop()
