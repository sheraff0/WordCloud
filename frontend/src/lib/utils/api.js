export const HOST = document.getElementById("static-host").innerText

const dataSetMap = dataSet => ({
  upload: {
    url: "/upload/"
  },
  checkHash: {
    url: "/check-hash/"
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
      print(response)
      update(state => ({ ...state, loading: false, error: response }))
      return
    }
    const jsonData = await response.json()
      .catch(err => new Error(err))
    const { detail, message } = jsonData;
  
    update(state => ({
      ...state, loading: false,
      ...(jsonData instanceof Error
        ? { error: jsonData }
        : detail || message
          ? { error: detail || message }
          : { data: jsonData, error: false }
      )
    }))
  })()
