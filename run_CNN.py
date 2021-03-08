

newCNN = CNN(0.5,[64,128],128,'relu')
newCNN.load_evaluation_data(image_list)
score = newCNN.evaluate_model()
score = score * 100.0
print(score)