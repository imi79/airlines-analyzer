"""Provider-neutral AI layer (decision 0005).

Every model call in the app goes through `LLM.call_tool`. The provider, the model for each job
and the name of the API key variable come from `config/models.yaml`; nothing outside this
package knows which vendor is used. The model must answer by filling one form (a "tool"), so
its output is structured data, never free text.
"""

from tearsheet.llm.base import LLMError, MissingKey, NotRecorded, ToolResult, ToolSpec, Usage
from tearsheet.llm.client import LLM
from tearsheet.llm.settings import ProviderSettings, load_settings

__all__ = [
    "LLM",
    "LLMError",
    "MissingKey",
    "NotRecorded",
    "ProviderSettings",
    "ToolResult",
    "ToolSpec",
    "Usage",
    "load_settings",
]
