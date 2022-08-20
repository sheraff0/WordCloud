import { CustomWritable } from './base'
import { fetchData } from "../utils/api"

const UPLOAD = "upload", CHECK_HASH = "checkHash"

// GENERIC DATASET

class DataSet extends CustomWritable {
  constructor(dataSet) {
    super({
      default: { loading: false, data: null },
      dataSet
    })
  }

  async loadData({ ...options } = {}) {
    await fetchData({ dataSet: this.dataSet, ...options })(this.update)
  }
}

// UPLOAD

class Upload extends DataSet {
  constructor() {
    super(UPLOAD)
    this.TEXT_FILE = "text_file"
  }

  extractData() {
    this.update(state => {
      const { data } = state
      const { counter=[], stopwords=[], wcloud=null } = data || {}
      return { ...state, counter, stopwords, wcloud }
    })
  }

  checkCounter() {
    this.update(state => {
      const { counter=[], stopwords=[] } = state
      const maxCount = Math.max(...counter.map(x => x[1]))
      const counterChecked = counter.map(x => {
        return ({
          active: (stopwords || []).indexOf(x[0]) > -1,
          text: x[0],
          size: Math.round(x[1] / maxCount * 100) / 100
        })
      })
      return { ...state, counterChecked }
    })
  }

  async loadAndCheck({ form, textParsed }) {
    if (textParsed) {
      const clone = form.cloneNode(true)
      const textField = clone.querySelector(`[name="${this.TEXT_FILE}"]`)
      textField.value = null
      await this.loadData({ form: clone })
    } else {
      await this.loadData({ form })
    }
    this.extractData()
    this.checkCounter()
  }

  updateStopwords(text, func) {
    this.update(state => {
      let { stopwords=[] } = state
      stopwords = func(stopwords, text)
      return { ...state, stopwords }
    })
    this.checkCounter()
  }

  addStopword(text) {
    this.updateStopwords(text, (stopwords, text) =>
      [...new Set([...(stopwords || []), text])]
    )
  }

  removeStopword(text) {
    this.updateStopwords(text, (stopwords, text) =>
      [...(stopwords || []).filter(x => x !== text)]
    )
  }

  resetStopwords(nullify=true) {
    this.updateStopwords("", (stopwords, text) =>
      nullify ? null: [])
  }

  resetWcloud() {
    this.update(state => ({ ...state, wcloud: null }))
  }
}

// CHECK HASH

class CheckHash extends DataSet {
  constructor() {
    super(CHECK_HASH)
  }

  extractData() {
    const { data } = this.getData()
    const { textParsed } = data || {}
    this.update(state => ({ ...state, textParsed }))
  }

  async loadAndCheck({ ...options }) {
    await this.loadData({ ... options })
    this.extractData()
  }
}

export const upload = new Upload()
export const checkHash = new CheckHash()
