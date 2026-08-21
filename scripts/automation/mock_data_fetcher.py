import json
import sys

def main():
    print(json.dumps({
        "competitors": [
            {
                "name": "Edthena",
                "strengths": ["Strong US presence", "Union-friendly", "Established rubric integration"],
                "weaknesses": ["Slow feedback loop", "Less automated AI", "High friction for teachers"],
                "business_model": "B2B SaaS to Districts/Schools",
                "architecture_assumptions": ["Monolithic web app", "Cloud video processing", "Human-in-the-loop coaching"]
            },
            {
                "name": "Vosaic",
                "strengths": ["Simple UX", "Good video annotation"],
                "weaknesses": ["Lack of deep AI insights", "Manual coding heavy"],
                "business_model": "B2B SaaS",
                "architecture_assumptions": ["Cloud-native", "Standard video pipelines"]
            }
        ],
        "papers": [
            {
                "title": "Multimodal Transformers for Classroom Activity Recognition",
                "year": 2023,
                "findings": "Fusing audio and visual modalities improves activity recognition by 15%."
            },
            {
                "title": "Affective Computing in Education: A Review",
                "year": 2022,
                "findings": "Emotion recognition is highly context-dependent and prone to bias in diverse classrooms."
            }
        ]
    }))

if __name__ == "__main__":
    main()
