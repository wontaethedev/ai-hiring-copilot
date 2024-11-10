import ulid

def generate_ulid() -> str:
  new_ulid = ulid.new()
  return str(new_ulid)
