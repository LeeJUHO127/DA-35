
import matplotlib.pyplot as plt
import torch 
from PIL import Image

def predict_image(image_path, model, transform, device):
    """
    image_path의 이미지를 model을 이용해서 추론.
    Parameter
        image_path: 추론할 이미지 경로
        model: 학습된 모델
        transform: 추론전 전처리 할 transform 
        device
    Return
        tuple: (class_index, 확률)
    """
    # 이미지 로딩
    img = Image.open(image_path)
    # 전처리
    input_data = transform(img)
    # batch 축 늘리기. (C, H, W) -> (1, C, H, W)
    input_data = input_data.unsqueeze(dim=0)
    input_data = input_data.to(device)

    # 추론
    model = model.to(device)
    model.eval()
    with torch.no_grad():
        pred = model(input_data).softmax(dim=-1)    # 추론결과(logit)을 확률값으로 변경.
        pred_class = pred.argmax(dim=-1).item()       # 정답 class
        pred_proba = pred.max(dim=-1).values.item() # 모델이 추정한 정답의 확률
        return pred_class, pred_proba  # 정답 class_index,  정답의 확률


def plot_fit_result(train_loss_list, train_accuracy_list, valid_loss_list, valid_accuracy_list):
    epoch = len(train_loss_list)
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(range(epoch), train_loss_list, label="train loss")
    plt.plot(range(epoch), valid_loss_list, label="validation loss")
    plt.title("Loss")
    plt.xlabel("epoch")
    plt.ylabel("loss")
    plt.grid(True, linestyle=':')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(range(epoch), train_accuracy_list, label="train accuracy")
    plt.plot(range(epoch), valid_accuracy_list, label="validation accuracy")
    plt.title("Accuracy")
    plt.xlabel("epoch")
    plt.ylabel("accuracy")
    plt.grid(True, linestyle=':')
    plt.legend()

    plt.tight_layout()
    plt.show()
