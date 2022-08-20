import { writable } from "svelte/store"


export class CustomWritable {
  constructor({ ...props }) {
    this.default = props.default
    const { subscribe, set, update } = writable(this.default)
    this.subscribe = subscribe, this.set = set, this.update = update
    Object.entries(props).forEach(prop => { this[prop[0]] = prop[1] })
  }

  reset() {
    this.set(this.default)
  }

  getData() {
    let result
    this.subscribe(state => result = state)()
    return result
  }
}
