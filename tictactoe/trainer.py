from train_data_loader import set_last_train_date, load_train_data
from model import get_model, save_model


def train():
    x_train, y_train, x_test, y_test = load_train_data()

    if len(x_train) == 0 or len(y_train) == 0:
        print("No new data to train on")
        exit(0)

    model = get_model()
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=10)
    save_model(model)

    test_loss, test_acc = model.evaluate(x_test, y_test)
    print('Test accuracy:', test_acc)

    set_last_train_date()


if __name__ == "__main__":
    train()