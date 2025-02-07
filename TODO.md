# Midjourney Parser Refactoring Plan

## 1. Structural Improvements (Phase 1)

- [ ] **Component Architecture:**

  ```python
  # New module structure
  parser/
  ├── __init__.py
  ├── core.py          # MidjourneyParser
  ├── parameters.py    # ParameterHandler
  ├── builder.py       # PromptBuilder
  ├── validation.py     # SchemaValidator
  └── exceptions.py    # Custom exceptions
  ```

- [ ] **Parameter Handler Class**

  ```python
  class ParameterHandler:
      def __init__(self):
          self.validators = ValidatorRegistry()
          self.converters = ConverterRegistry()
      
      def process(self, param_name: str, raw_value: Any) -> Any:
          """Unified parameter processing pipeline"""
          # Validation → Conversion → Type checking
  ```

## 2. Type Hint Modernization (Phase 1)

- [ ] **Generic Decorators**

  ```python
  P = ParamSpec("P")
  R = TypeVar("R")
  
  def validate_range(min_val: float, max_val: float) -> Callable[[Callable[P, R]], Callable[P, R]]:
      def decorator(func: Callable[P, R]) -> Callable[P, R]:
          @wraps(func)
          def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
              # Validation logic
              return func(*args, **kwargs)
          return wrapper
      return decorator
  ```

## 3. Validation Simplification (Phase 2)

- [ ] **Unified Validation Framework**

  ```python
  class ValidatorRegistry:
      _validators: dict[str, Callable] = {
          'range': lambda v, mn, mx: mn <= v <= mx,
          'version': validate_version_pattern,
          'image_ref': validate_image_reference
      }
      
      @classmethod
      def validate(cls, name: str, value: Any, *args) -> bool:
          return cls._validators[name](value, *args)
  ```

## 4. Parameter Handling (Phase 2)

- [ ] **Parameter Configuration Dataclass**

  ```python
  @dataclass(frozen=True)
  class ParameterConfig:
      name: str
      handler: Callable
      validator: Callable
      default: Any
      aliases: list[str] = field(default_factory=list)
      range: tuple[float, float] | None = None
  
  PARAMETER_CONFIGS = {
      'stylize': ParameterConfig(
          name='stylize',
          handler=handle_integer,
          validator=RangeValidator(STYLIZE_RANGE),
          default=DEFAULT_STYLIZE,
          aliases=['s']
      )
  }
  ```

## 5. Code Flow Improvements (Phase 3)

- [ ] **State Machine Implementation**

  ```python
  class ParserState(Enum):
      INITIALIZING = auto()
      PROCESSING_CORE = auto()
      HANDLING_REFERENCES = auto()
      VALIDATING = auto()
      FINALIZING = auto()
  
  class ParserStateMachine:
      def transition(self, new_state: ParserState):
          # State validation logic
  ```

## 6. Documentation (Phase 4)

- [ ] **Docstring Standards**

  ```python
  def process_aspect_ratio(value: str) -> tuple[int, int]:
      """Parse and validate aspect ratio string.
      
      Args:
          value: Input string in 'W:H' format
          
      Returns:
          Tuple of (width, height) integers
          
      Raises:
          ValueError: For invalid format or non-positive values
          
      Example:
          >>> process_aspect_ratio('16:9')
          (16, 9)
      """
  ```

## 7. Error Handling (Phase 3)

- [ ] **Exception Hierarchy**

  ```python
  class ParserError(Exception):
      """Base parser exception"""
  
  class ValidationError(ParserError):
      """Validation-related errors"""
  
  class ParameterValidationError(ValidationError):
      """Specific parameter validation failure"""
  ```

## 8. Modern Features (Phase 4)

- [ ] **Structural Pattern Matching**

  ```python
  def handle_version_param(value: str) -> str:
      match value.lower().split():
          case ['niji', version] if version in VALID_NIJI_VERSIONS:
              return f"niji {version}"
          case [version] if version in VALID_VERSIONS:
              return f"v{version}"
          case _:
              raise InvalidVersionError(value)
  ```

## 9. Testing Strategy

- [ ] **Test Matrix**

  | Test Type          | Coverage Target | Tools Used       |
  |--------------------|-----------------|------------------|
  | Parameter Validation | 100%           | pytest+hypothesis|
  | Error Conditions   | All error types | pytest.raises     |
  | Edge Cases         | Min/Max values  | hypothesis       |
  | Compatibility     | Legacy params   | pytest parametrize|

## 10. Deprecation Plan

1. Add deprecation warnings for old parameter names
2. Maintain legacy API with wrapper functions
3. Schedule removal for v2.0 release

## 11. Timeline Estimates

| Phase | Duration | Milestones                             |
|-------|----------|----------------------------------------|
| 1     | 2 weeks  | Core architecture in place             |
| 2     | 1.5 weeks| Parameter handling migrated            |
| 3     | 1 week   | Error handling implemented             |
| 4     | 1 week   | Documentation completed                |

## 12. First Implementation Steps

1. Create new `parser/parameters.py` with ParameterHandler
2. Migrate validation logic to ValidatorRegistry
3. Update MidjourneyParser to use new components
4. Write migration tests

**Next Action:** Should I proceed with implementing Phase 1 structural changes? Please toggle to Act Mode when ready.
