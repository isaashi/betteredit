import json
import numpy as np
from typing import Any, Dict
from datetime import datetime


class DesignRegistry:
    _registry: Dict[str, Any] = {}

    @classmethod
    def start_session(cls, session_id: str, config: dict):
        cls.register(
            module="Session Metadata",
            component="Session Info",
            concept="Session ID",
            technique="id",
            tuning_params={"session_id": session_id}
        )
        cls.register(
            module="Session Metadata",
            component="Session Info",
            concept="Timestamp",
            technique="time",
            tuning_params={"timestamp": datetime.utcnow().isoformat()}
        )
        cls.register(
           module="Session Metadata",
            component="Session Info",
            concept="Configuration",
            technique="settings",
            tuning_params=config
        )

    @classmethod
    def finish_session(cls):
        """
        Mark the end of the session by recording a final timestamp.
        """
        cls.register(
            module="Session Metadata",
            component="Session Info",
            concept="End Timestamp",
            technique="time",
            tuning_params={"timestamp": datetime.utcnow().isoformat()}
        )

    @classmethod
    def register(
        cls,
        module: str,
        component: str,
        concept: str,
        technique: str,
        tuning_params: Dict[str, Any]
    ) -> None:
        if module not in cls._registry:
            cls._registry[module] = {}
        if component not in cls._registry[module]:
            cls._registry[module][component] = {}
        if concept not in cls._registry[module][component]:
            cls._registry[module][component][concept] = {}
        if technique not in cls._registry[module][component][concept]:
            cls._registry[module][component][concept][technique] = {}

        cls._registry[module][component][concept][technique].update(tuning_params)

    @classmethod
    def get(cls, module: str) -> Dict[str, Any]:
        return cls._registry.get(module, {})

    @classmethod
    def full_registry(cls) -> Dict[str, Any]:
        return cls._registry

    @classmethod
    def to_json(cls, path: str = "outputs/design_registry.json") -> None:
        """
        Serialize the design registry to JSON, converting numpy arrays to lists.
        """
        def default(o: Any):
            if isinstance(o, np.ndarray):
                return o.tolist()
            return o

        with open(path, 'w') as f:
            json.dump(cls._registry, f, indent=2, default=default)
        print(f"[SAVED] Design registry saved to: {path}")

    @classmethod
    def pretty_print(cls) -> None:
        print("\n===== DESIGN REGISTRY =====")
        for module, components in cls._registry.items():
            print(f"\n[MODULE] {module}")
            if isinstance(components, dict):
                for component, concepts in components.items():
                    print(f"    [COMPONENT] {component}")
                    for concept, techniques in concepts.items():
                        print(f"        [CONCEPT] {concept}")
                        for technique, tuning in techniques.items():
                            print(f"            [TECHNIQUE] {technique}")
                            for param, value in tuning.items():
                                print(f"                [TUNING] {param}: {value}")
            else:
                # Session Metadata
                print(f"    {components}")