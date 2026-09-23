def make_reviews():

    reviews = [
        "The food was amazing",
        "I loved the food",
        "The restaurant was excellent",
        "The service was fantastic",
        "The meal was delicious",
        "Really good food and friendly staff",
        "I enjoyed everything",
        "The food was terrible",
        "I hated the food",
        "The restaurant was awful",
        "The service was horrible",
        "The meal was disgusting",
        "Really bad food and rude staff",
        "I regret eating here",
    ]

    labels = [
        1,  # positive
        1,
        1,
        1,
        1,
        1,
        1,

        0,  # negative
        0,
        0,
        0,
        0,
        0,
        0,
    ]

    return reviews, labels