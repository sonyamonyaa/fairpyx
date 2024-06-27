from experiments_csv import multi_plot_results


def multi_multi_plot_results(results_csv_file: str, save_to_file_template: str, filter: dict,
                             x_field: str, y_fields: list[str], z_field: str, mean: bool,
                             subplot_field: str, subplot_rows: int, subplot_cols: int, sharey: bool, sharex: bool,
                             legend_properties: dict):
    for y_field in y_fields:
        save_to_file = save_to_file_template.format(y_field)
        print(y_field, save_to_file)
        multi_plot_results(
            results_csv_file=results_csv_file,
            save_to_file=save_to_file,
            filter=filter,
            x_field=x_field, y_field=y_field, z_field=z_field, mean=mean,
            subplot_field=subplot_field, subplot_rows=subplot_rows, subplot_cols=subplot_cols, sharey=sharey,
            sharex=sharex,
            legend_properties=legend_properties,
        )


def plot_results_mma():
    """
    comparison plots between the two algorithms
    """
    filter = {"num_of_agents": 3,
              "algorithm": [
                  "divide_and_choose_for_three", "alloc_by_matching",
              ]}
    y_fields = ["utilitarian_value", "egalitarian_value",  # "egalitarian_utilitarian_ratio",
                "mean_envy", "runtime"]
    multi_multi_plot_results(
        results_csv_file="results/mma_comparison.csv",
        save_to_file_template="results/plots/mma_comparison_{}.png",
        filter=filter,
        x_field="value_noise_ratio", y_fields=y_fields, z_field="algorithm", mean=True,
        subplot_field="num_of_items", subplot_rows=3, subplot_cols=2, sharey=True, sharex=True,
        legend_properties={"size": 6},
    )


def plot_results_all_on_three():
    """
    comparison plots between divide and choose and the rest in the library
    """
    filter = {"num_of_agents": 3,
              "num_of_items": [250, 500, 750, 1000],
              "algorithm": [
                  "divide_and_choose_for_three",
                  "iterated_maximum_matching_unadjusted", "iterated_maximum_matching_adjusted",
                  "almost_egalitarian_without_donation", "almost_egalitarian_with_donation",
                  "round_robin", "bidirectional_round_robin"
              ]}

    y_fields = ["utilitarian_value", "egalitarian_value",
                # "egalitarian_utilitarian_ratio",
                "mean_envy", "runtime"]
    multi_multi_plot_results(
        results_csv_file="results/mma_comparison.csv",
        save_to_file_template="results/plots/mma_comparison_on_three_{}.png",
        filter=filter,
        x_field="value_noise_ratio", y_fields=y_fields, z_field="algorithm", mean=True,
        subplot_field="num_of_items", subplot_rows=2, subplot_cols=2, sharey=True, sharex=True,
        legend_properties={"size": 5},
    )


def plot_results_all_on_any():
    """
    comparison plots between alloc by matching and the rest in the library
    """
    filter = {"num_of_items": [250, 500, 750, 1000],
              "algorithm": [
                  "alloc_by_matching",
                  "iterated_maximum_matching_unadjusted", "iterated_maximum_matching_adjusted",
                  "almost_egalitarian_without_donation", "almost_egalitarian_with_donation",
                  "round_robin", "bidirectional_round_robin"
              ]}
    y_fields = ["utilitarian_value", "egalitarian_value",
                # "egalitarian_utilitarian_ratio",
                "mean_envy", "runtime"]
    multi_multi_plot_results(
        results_csv_file="results/mma_comparison.csv",
        save_to_file_template="results/plots/mma_comparison_on_any_{}.png",
        filter=filter,
        x_field="num_of_items", y_fields=y_fields, z_field="algorithm", mean=True,
        subplot_field="num_of_agents", subplot_rows=2, subplot_cols=2, sharey=True, sharex=True,
        legend_properties={"size": 5},
    )


if __name__ == "__main__":
    plot_results_mma()
    plot_results_all_on_three()
    plot_results_all_on_any()
