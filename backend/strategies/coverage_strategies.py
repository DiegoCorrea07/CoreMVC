from abc import ABC, abstractmethod

class ICoverageStatusStrategy(ABC):
    """
    La interfaz de Estrategia declara operaciones comunes a todas las versiones
    soportadas de un algoritmo. El Contexto usa esta interfaz para llamar al
    algoritmo definido por las Estrategias Concretas.
    """
    @abstractmethod
    def get_status(self, percentage: float) -> str | None:
        """
        Determina el estado basado en el porcentaje.
        Devuelve el nombre del estado si el porcentaje cae en su rango,
        o None si no lo hace.
        """
        pass

# --- Estrategias Concretas ---
# Cada clase implementa una variación del algoritmo.

class CriticalStatusStrategy(ICoverageStatusStrategy):
    """
    Estrategia para determinar el estado 'Crítica'.
    """
    def get_status(self, percentage: float) -> str | None:
        if 0 <= percentage < 70:
            return "Crítica"
        return None

class PartialStatusStrategy(ICoverageStatusStrategy):
    """
    Estrategia para determinar el estado 'Parcial'.
    """
    def get_status(self, percentage: float) -> str | None:
        if 70 <= percentage < 100:
            return "Parcial"
        return None

class CoveredStatusStrategy(ICoverageStatusStrategy):
    """
    Estrategia para determinar el estado 'Cubierta'.
    """
    def get_status(self, percentage: float) -> str | None:
        if percentage >= 100:
            return "Cubierta"
        return None