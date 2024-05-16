from shared.services.database_service import get_ml_config_count, get_tsd_config_count


class TrainDataFileResponse:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def get_data(self):
        return {
            "id": self.id,
            "name": self.name
        }


class TrainDataComplexResponse:
    def __init__(self, train_model, user, gaps: bool, length: int):
        self.train_model = train_model
        self.user = user
        self.gaps = gaps
        self.length = length

    def get_data(self):
        ml_count = get_ml_config_count(self.train_model.id, self.user.id)
        tsd_count = get_tsd_config_count(self.train_model.id, self.user.id)

        return {
            "id": self.train_model.id,
            "contains_gaps": self.gaps,
            "name": self.train_model.name,
            "created_at": self.train_model.created_at,
            "size": self.length,
            "ml_count": ml_count,
            "tsd_count": tsd_count
        }


class TrainDataResponse:
    def __init__(self, train_model, length: int):
        self.train_model = train_model
        self.length = length

    def get_data(self):
        return {
            "id": self.train_model.id,
            "name": self.train_model.name,
            "created_at": self.train_model.created_at,
            "size": self.length
        }


class PreviewDataResponse:
    def __init__(self, original: list, preview: list, flags: list):
        self.original = original
        self.preview = preview
        self.flags = flags

    def get_data(self):
        return {
            "original": {"name": "original", "values": self.original},
            "preview": {"name": "processed", "values": self.preview},
            "flags": self.flags
        }
