#!/usr/bin/env python

# Copyright 2018 Google LLC
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

import datetime
import os

from google.cloud import automl_v1beta1 as automl

import automl_vision_model

project_id = os.environ["GCLOUD_PROJECT"]
compute_region = "us-central1"


def test_model_create_status_delete(capsys):
    # create model
    client = automl.AutoMlClient()
    model_name = "test_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    project_location = client.location_path(project_id, compute_region)
    my_model = {
        "display_name": model_name,
        "dataset_id": "3946265060617537378",
        "image_classification_model_metadata": {"train_budget": 24},
    }
    response = client.create_model(project_location, my_model)
    operation_name = response.operation.name
    assert operation_name

    # get operation status
    automl_vision_model.get_operation_status(operation_name)
    out, _ = capsys.readouterr()
    assert "Operation status: " in out

    # cancel operation
    response.cancel()


def test_model_list_get_evaluate(capsys):
    # list models
    automl_vision_model.list_models(project_id, compute_region, "")
    out, _ = capsys.readouterr()
    list_models_output = out.splitlines()
    assert "Model id: " in list_models_output[2]

    # get model
    model_id = list_models_output[2].split()[2]
    automl_vision_model.get_model(project_id, compute_region, model_id)
    out, _ = capsys.readouterr()
    assert "Model name: " in out

    # list model evaluations
    automl_vision_model.list_model_evaluations(
        project_id, compute_region, model_id, ""
    )
    out, _ = capsys.readouterr()
    list_evals_output = out.splitlines()
    assert "name: " in list_evals_output[1]

    # get model evaluation
    model_evaluation_id = list_evals_output[1].split("/")[-1][:-1]
    automl_vision_model.get_model_evaluation(
        project_id, compute_region, model_id, model_evaluation_id
    )
    out, _ = capsys.readouterr()
    assert "evaluation_metric" in out
