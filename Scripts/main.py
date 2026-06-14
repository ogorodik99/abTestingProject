import importlib
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

gui = importlib.import_module("Scripts.gui")
data_manager = importlib.import_module("Scripts.data_manager")
analysis = importlib.import_module("Scripts.analysis")
reports = importlib.import_module("Scripts.reports")
CFG = importlib.import_module("Scripts.config").CFG
ensure_dirs = importlib.import_module("Library.utils").ensure_dirs

LAST_FULL_RESULT = None


def handle_analysis():
    csv_path = os.path.join(CFG["data_dir"], "ab_data.csv")
    return handle_csv_analysis(csv_path)


def handle_csv_analysis(csv_path):
    global LAST_FULL_RESULT

    result = analysis.run_ctr_analysis(csv_path)
    graph_path = reports.save_ctr_graph(result, CFG["graphics_dir"])
    result["graph_path"] = graph_path
    LAST_FULL_RESULT = result

    report_path = os.path.join(CFG["output_dir"], "ctr_report.txt")
    with open(report_path, "w", encoding="utf-8") as file:
        file.write(result["text"])

    print(result["text"])
    return {
        "text": result["text"],
        "graph_path": graph_path,
    }


def show_full_plots():
    if LAST_FULL_RESULT is None:
        handle_analysis()

    reports.show_ctr_graph(LAST_FULL_RESULT)


def load_ab_data():
    return data_manager.load_ab_data(CFG["data_dir"])


def save_ab_data(data):
    data_manager.save_ab_data(CFG["data_dir"], data)


def main():
    ensure_dirs([CFG["data_dir"], CFG["output_dir"], CFG["graphics_dir"]])
    app = gui.create_main_window(
        handle_analysis,
        handle_csv_analysis,
        show_full_plots,
        load_ab_data,
        save_ab_data,
    )
    app.mainloop()


if __name__ == "__main__":
    main()
