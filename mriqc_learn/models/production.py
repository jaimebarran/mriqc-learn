# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# Copyright 2021 The NiPreps Developers <nipreps@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# We support and encourage derived works from this project, please read
# about our expectations at
#
#     https://www.nipreps.org/community/licensing/
#
"""Create a pipeline for nested cross-validation."""
from pkg_resources import resource_filename as pkgrf

from joblib import load
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier as RFC
from mriqc_learn.models import preprocess as pp


def load_model():
    return load(pkgrf("mriqc_learn.data", "classifier.joblib"))


def init_pipeline():
    """Initialize the pipeline."""
    steps = [
        (
            "drop_ft",
            pp.DropColumns(
                drop=[f"size_{ax}" for ax in "xyz"] + [f"spacing_{ax}" for ax in "xyz"]
            ),
        ),
        (
            "drop_brainIQMs",
            pp.DropColumns(
                drop=[
                    "cjv",
                    "cnr",
                    # "efc",
                    # "fber",
                    # "fwhm_avg",
                    # "fwhm_x",
                    # "fwhm_y",
                    # "fwhm_z",
                    "icvs_csf",
                    "icvs_gm",
                    "icvs_wm",
                    # "inu_med",
                    # "inu_range",
                    # "qi_1",
                    # "qi_2",
                    "rpve_csf",
                    "rpve_gm",
                    "rpve_wm",
                    "snr_csf",
                    "snr_gm",
                    "snr_total",
                    "snr_wm",
                    "snrd_csf",
                    "snrd_gm",
                    # "snrd_total",
                    "snrd_wm",
                    "summary_bg_k",
                    "summary_bg_mad",
                    "summary_bg_mean",
                    "summary_bg_median",
                    "summary_bg_n",
                    "summary_bg_p05",
                    "summary_bg_p95",
                    "summary_bg_stdv",
                    "summary_csf_k",
                    "summary_csf_mad",
                    "summary_csf_mean",
                    "summary_csf_median",
                    "summary_csf_n",
                    "summary_csf_p05",
                    "summary_csf_p95",
                    "summary_csf_stdv",
                    "summary_gm_k",
                    "summary_gm_mad",
                    "summary_gm_mean",
                    "summary_gm_median",
                    "summary_gm_n",
                    "summary_gm_p05",
                    "summary_gm_p95",
                    "summary_gm_stdv",
                    "summary_wm_k",
                    "summary_wm_mad",
                    "summary_wm_mean",
                    "summary_wm_median",
                    "summary_wm_n",
                    "summary_wm_p05",
                    "summary_wm_p95",
                    "summary_wm_stdv",
                    "tpm_overlap_csf",
                    "tpm_overlap_gm",
                    "tpm_overlap_wm",
                    "wm2max"
                ]
            ),
        ),
        (
            "scale",
            pp.SiteRobustScaler(
                with_centering=True,
                with_scaling=True,
                unit_variance=True,
            ),
        ),
        ("site_pred", pp.SiteCorrelationSelector()),
        ("winnow", pp.NoiseWinnowFeatSelect(use_classifier=True)),
        ("drop_site", pp.DropColumns(drop=["site"])),
        (
            "rfc",
            RFC(
                bootstrap=True,
                class_weight=None,
                criterion="gini",
                max_depth=10,
                max_features="sqrt",
                max_leaf_nodes=None,
                min_impurity_decrease=0.0,
                min_samples_leaf=10,
                min_samples_split=10,
                min_weight_fraction_leaf=0.0,
                n_estimators=400,
                oob_score=True,
            ),
        ),
    ]

    return Pipeline(steps)
