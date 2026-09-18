import numpy as np

try:
    # Lightweight runtime normally used on the portable controller
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    # Development-computer fallback
    from tensorflow.lite import Interpreter
    
def lstm_test_cob(SS):
    """
    Add the newest feature vector to the rolling window and predict
    the current kinematics.
    """
    SS["lstm_feat_mean"] = False
    # Skip prediction while mimic training is occurring.
    if SS.get("train_iter") is not None:
        return SS

    indices = np.asarray(
        SS["sel_feat_idx"],
        dtype=np.intp
    ).reshape(-1)

    # Convert the current features into one flat feature vector.
    all_features = np.asarray(
        SS["feat"],
        dtype=np.float32
    ).reshape(-1)

    z = SS['feat']
    
    #z = np.concatenate((
    #np.asarray(SS['d'][0:32,1]).reshape(-1),
    #np.asarray(SS['feat']).reshape(-1)
    #))

    expected_features = SS["lstm_feature_count"]

    if z.size != expected_features:
        raise ValueError(
            f"Current z contains {z.size} features, but the model "
            f"expects {expected_features}."
        )

    # -------------------------------------------------------------
    # Apply the exact same feature normalization used during training.
    #
    # Do not normalize here when normalization was included as a
    # layer inside the exported model.
    # -------------------------------------------------------------
    if (
        "lstm_feat_mean" in SS and
        "lstm_feat_std" in SS
    ):
        feat_mean = np.asarray(
            SS["lstm_feat_mean"],
            dtype=np.float32
        ).reshape(-1)

        feat_std = np.asarray(
            SS["lstm_feat_std"],
            dtype=np.float32
        ).reshape(-1)

        if feat_mean.size != z.size or feat_std.size != z.size:
            raise ValueError(
                "The saved feature normalization arrays do not match z."
            )

        # Protect against a zero standard deviation.
        safe_std = np.where(feat_std == 0, 1.0, feat_std)
        z = (z - feat_mean) / safe_std

    # -------------------------------------------------------------
    # Update rolling window
    # -------------------------------------------------------------
    z_window = SS["lstm_z_window"]

    z_window[:-1, :] = z_window[1:, :]
    z_window[-1, :] = z

    SS["lstm_samples_seen"] += 1

    # Safest behavior is to command zero until a complete real window
    # has been collected.
    if SS["lstm_samples_seen"] < SS["lstm_window_size"]:
        SS["xhat_raw"] = np.zeros(
            (7, 1),
            dtype=np.float32
        )
        SS["xhat"] = SS["xhat_raw"].copy()
        return SS

    # Add batch dimension:
    # [time, features] -> [1, time, features]
    model_input = z_window[np.newaxis, :, :].astype(
        np.float32,
        copy=False
    )
    
    interpreter = SS["lstm_interpreter"]
    input_info = SS["lstm_input_info"]
    output_info = SS["lstm_output_info"]

    interpreter.set_tensor(
        input_info["index"],
        model_input
    )

    interpreter.invoke()
    
    prediction = interpreter.get_tensor(
        output_info["index"]
    )
    # print("SS['feat'] shape:", np.asarray(prediction).shape)
    # Support either:
    # many-to-one output:  [1, number_of_dofs]
    # sequence output:     [1, time, number_of_dofs]
    if prediction.ndim == 3:
        prediction = prediction[0, -1, :]
       
    elif prediction.ndim == 2:
        prediction = prediction[0, :]
        
    else:
        prediction = prediction.reshape(-1)

    prediction = prediction.astype(np.float32)

    # Undo output normalization only when the model was trained using
    # normalized targets and does not already include this operation.
    #if (
    #    "lstm_kin_mean" in SS and
    #    "lstm_kin_std" in SS
    #):
    #    kin_mean = np.asarray(
    #        SS["lstm_kin_mean"],
    #        dtype=np.float32
    #    ).reshape(-1)

    #    kin_std = np.asarray(
    #        SS["lstm_kin_std"],
     #       dtype=np.float32
      #  ).reshape(-1)

        #prediction = prediction * kin_std + kin_mean

    # Match the existing controller's normalized command range.
    # Disable this only if the model predicts physical units rather
    # than normalized -1 to +1 commands.
    if SS.get("lstm_clip_output", True):
        SS["xhat_raw"] = np.clip(prediction, -1.0, 1.0)

        
    if SS["lstm_feature_count"] == 528:
        selected = np.asarray(prediction).reshape(-1)[[0, 1, 2, 5, 9, 11]]
        SS["xhat_raw"] = np.concatenate(
        (selected, np.array([0], dtype=selected.dtype))
        ).reshape(-1, 1)
    else:
        SS["xhat_raw"] = np.asarray(prediction).reshape(-1)[[0, 1, 2, 3,4,5,6]]
       

    
    SS["xhat"] = SS["xhat_raw"].copy()
    
    return SS