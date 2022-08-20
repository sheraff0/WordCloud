import { md5 } from 'hash-wasm'
import { writable } from 'svelte/store'

// STORE VARIABLE FOR HASHES

export const hashes = writable({})


// GENERIC FILE INPUT

class FileInput {
  constructor(input) {
    this.name = input.getAttribute("name")
    this.files = input.files
    this.results = {}
  }

  readFile(index=0) {
    const file = this.files[index]
    if (!file) return;
    const reader = new FileReader()
    reader.readAsBinaryString(file)
    reader.onload = () => this.onLoad(reader, index)
  }

  onLoad(reader, index) {
    this.results[index] = reader.result
  }
}


// HASHED FILE INPUT

class HashedFileInput extends FileInput {
  constructor(input) {
    super(input)
    this.updateHashes({
      ready: false
    })
  }

  async onLoad(reader, index) {
    super.onLoad(reader, index)
    const hash = await md5(this.results[index])
    this.updateHashes({
      [index]: hash,
      ready: true
    })
  }

  updateHashes(obj) {
    hashes.update(state => {
      const { [this.name]: scope } = state || {}
      return { ...state, [this.name]: { ...scope, ...obj } }
    })
  }

}


function hashFileData(e) {
  const fileInput = new HashedFileInput(e.target)
  fileInput.readFile()
}


export function hashFile(node) {
  node.addEventListener("change", hashFileData)
  return {
    destroy() {
      node.removeEventListener("change", hashFileData)
    }
  }
}
