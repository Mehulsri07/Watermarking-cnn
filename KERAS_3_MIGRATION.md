# Keras 3.12 Migration Guide

## Changes Made for Keras 3.12 Compatibility

### 1. Requirements Update (`requirements.txt`)

**Changed:**
- `tensorflow>=2.8.0` → `tensorflow>=2.16.0`
- Added explicit `keras>=3.0.0` dependency
- `numpy>=1.19.5,<2.0` → `numpy>=1.23.0,<2.0`
- Removed `tensorflow-addons` (deprecated in TF 2.16+)

**Reason:** Keras 3.12 requires TensorFlow 2.16+ and has different dependency requirements.

### 2. Attack Simulator Update (`models/wavetf_model.py`)

**Changed:**
- Replaced deprecated `tf.switch_case` with nested `tf.cond` statements

**Before:**
```python
condition = Lambda(lambda x: tf.switch_case(
    x[0][0],
    branch_fns={
        0: lambda: stupid_function(x[1]),
        1: lambda: combined_attack_function(x[1]),
        # ...
    },
    default=lambda: stupid_function(x[1])
))((attack_id_layer[0], image_layer))
```

**After:**
```python
def apply_attack(inputs):
    attack_id, image = inputs
    attack_id_scalar = attack_id[0]
    
    result = tf.cond(
        tf.equal(attack_id_scalar, 0),
        lambda: stupid_function(image),
        lambda: tf.cond(
            tf.equal(attack_id_scalar, 1),
            lambda: combined_attack_function(image),
            # ... nested conditions
        )
    )
    return result

condition = Lambda(apply_attack)((attack_id_layer, image_layer))
```

**Reason:** `tf.switch_case` was deprecated in TensorFlow 2.x and removed in Keras 3.x. The nested `tf.cond` approach is the recommended replacement.

### 3. Model Saving Format (`train_and_evaluate.py`)

**Changed:**
- `final_model_weights.h5` → `final_model_weights.keras`

**Reason:** The `.h5` format is deprecated in Keras 3.x. The new `.keras` format is the native Keras 3 format and provides better compatibility.

## Migration Benefits

1. **Future-proof:** Compatible with latest Keras 3.12 and TensorFlow 2.16+
2. **Better performance:** Keras 3 includes performance optimizations
3. **Improved stability:** Uses officially supported APIs
4. **Native format:** `.keras` format is more reliable than legacy `.h5`

## Testing Recommendations

After migration, test the following:

1. **Model training:** Verify training runs without errors
2. **Attack simulation:** Test all 6 attack types (0-5)
3. **Model saving/loading:** Ensure weights save and load correctly
4. **Evaluation:** Run full evaluation suite

## Backward Compatibility Notes

- Old `.h5` weight files can still be loaded with `model.load_weights('old_file.h5')`
- New `.keras` files are NOT compatible with TensorFlow < 2.16
- If you need to support older TensorFlow versions, keep the old code

## Installation

To install updated dependencies:

```bash
cd watermark-cnn
pip install -r requirements.txt --upgrade
```

## Verification

Check your installation:

```python
import tensorflow as tf
import keras

print(f"TensorFlow version: {tf.__version__}")
print(f"Keras version: {keras.__version__}")

# Should show TensorFlow >= 2.16.0 and Keras >= 3.0.0
```

## Known Issues

1. **tensorflow-addons:** Removed from requirements as it's deprecated. If you need specific addons functionality, consider alternatives or pin to older TF versions.

2. **NumPy 2.0:** Currently limited to NumPy < 2.0 for compatibility. This may be relaxed in future TensorFlow releases.

## Support

If you encounter issues:
1. Check TensorFlow/Keras version compatibility
2. Verify all dependencies are updated
3. Clear any cached model files
4. Reinstall requirements from scratch if needed

---

**Migration Date:** 2025-11-23
**Target Versions:** TensorFlow 2.16+, Keras 3.12+
