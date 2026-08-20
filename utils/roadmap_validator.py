def validate_roadmap(roadmap):

    required_fields = [
        "career",
        "roadmap_summary",
        "phases",
        "final_project"
    ]

    for field in required_fields:
        if field not in roadmap:
            raise ValueError(
                f"Missing required field: {field}"
            )

    if not isinstance(roadmap["phases"], list):
        raise ValueError("phases must be a list")

    if len(roadmap["phases"]) == 0:
        raise ValueError("Roadmap must contain at least one phase")

    phase_fields = [
        "phase",
        "skill",
        "reason",
        "topics",
        "mini_project"
    ]

    for phase in roadmap["phases"]:

        for field in phase_fields:
            if field not in phase:
                raise ValueError(
                    f"Missing phase field: {field}"
                )

        if not isinstance(phase["topics"], list):
            raise ValueError(
                "topics must be a list"
            )

        if len(phase["topics"]) == 0:
            raise ValueError(
                f"Phase {phase['phase']} must contain topics"
            )

    final_project_fields = [
        "title",
        "description",
        "skills_used",
        "expected_outcome"
    ]

    for field in final_project_fields:
        if field not in roadmap["final_project"]:
            raise ValueError(
                f"Missing final project field: {field}"
            )

    return True