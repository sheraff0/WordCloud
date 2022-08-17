export const HOST = "http://127.0.0.1:8000/";

const dataSetMap = dataSet => ({
  upload: {
    url: "/upload"
  }
})[dataSet]

const getRequestOptions = ({ form, data }) => {
  let body
  if (form) {
    body = new FormData(form)
    return { body }
  } else if (data) {
    body = JSON.stringify(data)
    return {
      body,
      headers: { 'Content-Type': 'application/json' }
    }
  } else { return {} }
}

export const fetchData = ({ dataSet, form, data, method="POST" }) => update =>
  (async () => {
    const { url } = dataSetMap(dataSet)
    update(state => ({ ...state, loading: true }))
    const options = getRequestOptions({ form, data })
    const response = await fetch(url, { method, ...options })
      .catch(err => new Error(err))

    if (response instanceof Error) {
      update(state => ({ ...state, loading: false, error: response }))
      return
    }

    const jsonData = await response.json()
      .catch(err => new Error(err))

    update(state => ({
      ...state, loading: false,
      ...(data instanceof Error
        ? { error: jsonData }
        : { data: jsonData, error: false })
    }))
  })()
