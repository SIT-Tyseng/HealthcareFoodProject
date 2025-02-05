import statistics

CLASS_NAMES = ['Mass']


def N5K_Metric(phase, groundtruth_values, prediction_data):
    log_stats = {}
    MAE_Percentage_sum = []
    for i, field in enumerate(CLASS_NAMES):
        abs_err = [abs(p - g)
                   for g, p in zip(groundtruth_values[field], prediction_data[field])]
        mae = statistics.mean(abs_err)
        log_stats[f"{phase} MAE {field}"] = mae
        log_stats[f"{phase} MAE_% {field}"] = (
                    100 * log_stats[f"{phase} MAE {field}"] / statistics.mean(groundtruth_values[field]))
        MAE_Percentage_sum.append(log_stats[f"{phase} MAE_% {field}"])

    log_stats[f"{phase} MAE_% Mean"] = sum(MAE_Percentage_sum) / 5
    return log_stats
