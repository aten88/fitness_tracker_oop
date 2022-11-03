class InfoMessage:
    """Информационный класс сообщения о тренировке."""
    def __init__(self, training_type: str, duration: int, distance: int,
                 speed: int, calories: float):
        self.type_training = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Методы вывода сообщений на экран"""
        return (f'Тип тренировки: { self.type_training};'
                f' Длительность: { self.duration:.3f} ч.;'
                f' Дистанция: { self.distance:.3f} км;'
                f' Ср. скорость: { self.speed:.3f} км/ч;'
                f' Потрачено ккал: { self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.type_training = 'Base'

    def get_distance(self) -> float:
        """Метод для получения дистанции в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Метод для получения средн. скорости движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Метод для получения количества затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Метод возврата информационного сообщения о тренировке."""
        return InfoMessage(self.type_training,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action: int, duration: int, weight: int):
        super().__init__(action, duration, weight)
        self.type_training = 'Running'

    def get_spent_calories(self) -> float:
        """Собственный метод подсчета каллорий Running"""
        return (((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                 * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self, action: int, duration: int, weight: int, height: int):
        super().__init__(action, duration, weight)
        self.height = height
        self.type_training = 'SportsWalking'

    def get_spent_calories(self) -> float:
        """Собственный метод подсчета каллорий SportsWalking"""
        return (
               ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((Training.get_mean_speed(self) * self.KMH_IN_MSEC)**2
                 / (self.height / self.CM_IN_M))
                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * self.duration * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: float = 2

    def __init__(self, action: int, duration: int, weight: int,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.type_training = 'Swimming'

    def get_mean_speed(self) -> float:
        """Собственный метод подсчета ср/скорости  Swimming"""
        return ((self.length_pool * self.count_pool) / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Собственный метод подсчета каллорий Swimming"""
        return ((Swimming.get_mean_speed(self)
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Функция чтения данных полученных от датчиков."""
    dict_data: dict = {'SWM': Swimming,
                       'RUN': Running,
                       'WLK': SportsWalking
                       }
    if workout_type in dict_data:
        object = dict_data[workout_type](*data)
        return object


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
