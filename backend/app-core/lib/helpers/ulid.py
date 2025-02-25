import ulid

def generate_ulid() -> str:
  """
  Generates a ULID
  """

  new_ulid = ulid.new()
  return str(new_ulid)
