# AI Fall Detection Project

An end-to-end fall detection system that processes human activity video and predicts **Fall** or **Not Fall**.

## Project Pipeline

```text
RGB Frames
   ↓
Human Detection
   ↓
Pose / Temporal Feature Extraction
   ↓
ML Fall Classifier
   ↓
Backend API
   ↓
Frontend
```

The project uses the **UR Fall Detection Dataset** for development and prototyping. Raw RGB sequences are used for the vision pipeline, while the extracted UR Fall feature CSV is used as an early ML prototype dataset.

> The extracted UR Fall features are **not assumed to be the final features** used by the complete system.  
> The final classifier input will depend on the temporal features produced by the Pose & Feature Engineering stage.

## Team

| Area | Owner(s) | Responsibility |
|---|---|---|
| Human Detection | Malak | Detect the person in RGB frames and produce bounding boxes |
| Pose & Feature Engineering | Salma + Jana | Extract keypoints and temporal movement features |
| ML / Classifier | Ahmed + Farida | Train, evaluate, save, and document the Fall / Not Fall classifier |
| Backend | Ahmed + Andrew | Expose the trained model through an inference API |
| Frontend | Malak + Jana | Display prediction results and connect to the backend |

## Project Timeline

| Week | Main Goal |
|---|---|
| Week 1 | Dataset setup, data understanding, contracts, and first prototypes |
| Week 2 | Human detection and pose/keypoint extraction |
| Week 3 | Feature dataset, baseline classifier, and backend skeleton |
| Week 4 | Temporal model improvement and pipeline integration |
| Week 5 | Freeze features/model and stabilize backend/frontend integration |
| Week 6 | End-to-end testing, debugging, documentation, and final demo |

## Data Flow and Handoffs

### 1. Human Detection Output

The detection stage should preserve the frame identity and return information similar to:

```text
sequence_id
frame_id
frame_reference
x1
y1
x2
y2
detection_confidence
```

### 2. Pose / Feature Output

The pose team converts movement across frames into numerical temporal features.

Example structure:

```text
sequence_id
window_id
start_frame
end_frame
feature columns...
fall_target
```

Candidate features may include body angle, movement speed, vertical displacement, hip height, bounding-box ratio, and stay-down duration.

### 3. ML Model Package

The ML stage should eventually provide:

```text
saved model
preprocessing/scaler if used
ordered feature list
classification threshold
class mapping
example input
example output
model version
```

Binary target:

```text
1 = Fall
0 = Not Fall / ADL
```

### 4. Backend Response

A final backend response may contain:

```json
{
  "prediction": "Fall",
  "confidence": 0.91,
  "model_version": "v1"
}
```

## Week 1

Week 1 focuses on understanding the data and defining how the different project stages will communicate.

For the ML team, the first prototype includes:

- loading and inspecting the UR Fall extracted-feature CSV
- understanding the dataset columns and original posture labels
- checking missing values and duplicates
- basic exploratory data analysis
- defining the binary project target: **Fall / Not Fall**
- preparing a cleaned prototype dataset
- defining the expected classifier input

The Week 1 notebook and generated dataset are kept as the starting point for ML experimentation.

## Important Team Rules

1. Preserve `sequence`, `frame`, and `window` identifiers for debugging and handoffs.
2. Document any coordinate, unit, normalization, or column-name transformation.
3. Avoid train/test leakage between highly related frames or windows from the same sequence.
4. Version frozen artifacts such as feature schemas, models, and API contracts.
5. Communicate feature-definition changes to the ML team.
6. Communicate model-input changes to the backend team.
7. Integration should happen progressively rather than waiting until the final week.

## Project Documentation

The detailed timeline, responsibilities, handoff contracts, weekly tasks, and acceptance criteria are maintained in Notion:

**[Fall Detection — Full Team Timeline & Handover Guide](https://app.notion.com/p/Fall-Detection-Full-Team-Timeline-Handover-Guide-3e6c52e9fae58179b0cbc61832cdc2f9?source=copy_link)**

The Notion guide is the main reference for the current agreed workflow and team handoffs.

## Dataset

**UR Fall Detection Dataset**

The dataset contains fall and Activities of Daily Living (ADL) sequences and includes RGB/depth recordings and sensor information.

Official reference:

https://www.fenix.ur.edu.pl/~mkepski/ds/uf.html

## Final Goal

The final system should allow a test sequence to pass through the complete pipeline:

```text
Video / Frames
→ Human Detection
→ Pose / Temporal Features
→ Fall Classifier
→ Backend API
→ Frontend
→ Fall / Not Fall Result
```

without manually rewriting intermediate files between stages.
