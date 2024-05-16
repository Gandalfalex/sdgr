import numpy as np
import functools
import tsgm.dataset
import tsgm.metrics
import sklearn.metrics
import sklearn.svm


class SyntheticDataEvaluation:

    def __init__(self, real_dataset, synthetic_dataset):
        """
        :param real_dataset: The real dataset used for training and evaluation.
        :param synthetic_dataset: The synthetic dataset used for training and evaluation.

        """
        self.real_dataset = real_dataset
        self.synthetic_dataset = synthetic_dataset
        self.seq_len, self.feat_dim, self.n_classes = *real_dataset.shape[1:], 2

        statistics = [functools.partial(tsgm.metrics.statistics.axis_max_s, axis=None),
                      functools.partial(tsgm.metrics.statistics.axis_min_s, axis=None),
                      functools.partial(tsgm.metrics.statistics.axis_max_s, axis=1),
                      functools.partial(tsgm.metrics.statistics.axis_min_s, axis=1)]
        discrepancy_func = lambda x, y: np.linalg.norm(x - y)
        self.sim_metric = tsgm.metrics.DistanceMetric(
            statistics=statistics, discrepancy=discrepancy_func
        )

        models = [tsgm.models.zoo["clf_cl_n"](self.seq_len, self.feat_dim, self.n_classes, n_conv_lstm_blocks=i) for i
                  in range(1, 4)]
        for m in models:
            m.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.evaluators = [self.EvaluatorConvLSTM(m.model) for m in models]

        self.consistency_metric = tsgm.metrics.ConsistencyMetric(evaluators=self.evaluators)

        downstream_model = tsgm.models.zoo["clf_cl_n"](self.seq_len, self.feat_dim, self.n_classes,
                                                       n_conv_lstm_blocks=1).model
        downstream_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.evaluator = self.EvaluatorConvLSTM(downstream_model)
        self.downstream_perf_metric = tsgm.metrics.DownstreamPerformanceMetric(self.evaluator)

        self.attacker = self.FlattenTSOneClassSVM(sklearn.svm.OneClassSVM())
        self.privacy_metric = tsgm.metrics.PrivacyMembershipInferenceMetric(attacker=self.attacker)

    class EvaluatorConvLSTM:
        """
        Class to evaluate a ConvLSTM model.

        Attributes:
            _model (object): The ConvLSTM model.

        Methods:
            __init__(model): Initializes the EvaluatorConvLSTM instance.
            evaluate(D, D_test): Evaluates the model using the given datasets.

        """

        def __init__(self, model):
            self._model = model

        def evaluate(self, D: tsgm.dataset.Dataset, D_test: tsgm.dataset.Dataset) -> float:
            X_train, y_train = D.Xy
            X_test, y_test = D_test.Xy
            self._model.fit(X_train, y_train)
            y_pred = np.argmax(self._model.predict(X_test), axis=1)
            y_test = np.argmax(y_test, axis=1)
            return sklearn.metrics.accuracy_score(y_pred, y_test)

    class FlattenTSOneClassSVM:
        def __init__(self, clf):
            self._clf = clf

        def fit(self, X):
            X_fl = X.reshape(X.shape[0], -1)
            self._clf.fit(X_fl)

        def predict(self, X):
            X_fl = X.reshape(X.shape[0], -1)
            return self._clf.predict(X_fl)

    def evaluate(self, test_dataset=None):
        sim = self.sim_metric(self.real_dataset, self.synthetic_dataset)
        consistency = self.consistency_metric(self.real_dataset, self.synthetic_dataset, self.real_dataset)
        downstream_perf = self.downstream_perf_metric(self.real_dataset, self.synthetic_dataset, self.real_dataset)

        if test_dataset is not None:
            privacy = self.privacy_metric(self.real_dataset, self.synthetic_dataset, test_dataset)
            return {
                "similarity": sim,
                "consistency": consistency,
                "downstream": downstream_perf,
                "privacy": privacy
            }
        return {
            "similarity": sim,
            "consistency": consistency,
            "downstream": downstream_perf
        }
