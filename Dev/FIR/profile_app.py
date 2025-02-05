import cProfile
import pstats
import os
from aiModel import analyze_image

# Set the image path and input text for profiling
image_path = r"C:\Users\Kingston\PycharmProjects\AITraining\research_dataset\Apple\0IUM3IJH8Y1HOSS2CCPS36YY.jpg"
input_text = ""  # or provide some text input if needed

# Create a profile object
pr = cProfile.Profile()

# Enable the profiler
pr.enable()

# Call the function to be profiled
food_item, advice_result = analyze_image(image_path, input_text)

# Disable the profiler
pr.disable()

# Print the results
stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME)
stats.print_stats()

# Print the output
print(f"Food Item: {food_item}")
print(f"Advice: {advice_result}")
