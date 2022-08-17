import { writable } from "svelte/store"
import { fetchData } from "./api"

const UPLOAD = "upload"

// GENERIC DATASET

class DataSet {
  constructor(dataSet) {
    this.dataSet = dataSet
    const { subscribe, set, update } = writable({ loading: false, data: null })
    this.subscribe = subscribe; this.set = set; this.update = update
  }

  reset() {
    this.set({ loading: false, data: null })
  }

  async loadData({ ...options } = {}) {
    await fetchData({ dataSet: this.dataSet, ...options })(this.update)
  }

  getData() {
    let result
    this.subscribe(state => result = state)()
    return result
  }
}

// UPLOAD

class Upload extends DataSet {
  constructor() {
    super(UPLOAD)
  }

  extractData() {
    const { data } = this.getData()
    const { counter=[], stopwords=[] } = data || {}
    this.update(state => ({ ...state, counter, stopwords }))
  }

  checkCounter() {
    const { counter=[], stopwords=[] } = this.getData()
    const maxCount = Math.max(...counter.map(x => x[1]))
    const counterChecked = counter.map(x => {
      return ({
        active: stopwords.indexOf(x[0]) > -1,
        text: x[0],
        size: Math.round(x[1] / maxCount * 100) / 100
      })
    })
    this.update(state => ({ ...state, counterChecked }))
  }

  async loadAndCheck({ ...options }) {
    await this.loadData({ ...options })
    this.extractData()
    this.checkCounter()
  }

  updateStopwords(text, func) {
    let { stopwords=[] } = this.getData()
    stopwords = func(stopwords, text)
    this.update(state => ({ ...state, stopwords }))
    this.checkCounter()
  }

  addStopword(text) {
    this.updateStopwords(text, (stopwords, text) =>
      [...new Set([...stopwords, text])]
    )
  }

  removeStopword(text) {
    this.updateStopwords(text, (stopwords, text) =>
      [...stopwords.filter(x => x !== text)]
    )
  }
}

export const upload = new Upload()