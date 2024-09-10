using System;
using UnityEngine;
using System.Collections;
using UnityEngine.Networking;

public class SendAndRecieveServerEvents : MonoBehaviour
{
	void OnEnable ()
	{
		Vector3Value value = new Vector3Value("Cube", "location", new _Vector3(2, 2, 2));
		string jsonText = JsonUtility.ToJson(value);
		StartCoroutine(JsonEvent (jsonText));
	}

	void Update ()
	{
		if (Input.GetMouseButtonDown(0))
		{
			Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
			RaycastHit hit;
			if (Physics.Raycast(ray.origin, ray.direction, out hit, Mathf.Infinity, 1 << 31, QueryTriggerInteraction.Collide))
				StartCoroutine(OnClickEvent (hit.collider.name));
		}
	}

	IEnumerator OnClickEvent (string objectName)
	{
		UnityWebRequest webRequest = UnityWebRequest.Get("http://localhost:8000/" + objectName);
		yield return webRequest.SendWebRequest();
		if (webRequest.result == UnityWebRequest.Result.Success)
			print("Web request result: " + webRequest.downloadHandler.text);
		else
			print(webRequest.error);
	}


	IEnumerator JsonEvent (string jsonText)
	{
		UnityWebRequest webRequest = UnityWebRequest.Get("http://localhost:8000/exec?" + jsonText.Base64Encode());
		yield return webRequest.SendWebRequest();
		if (webRequest.result == UnityWebRequest.Result.Success)
			print("Web request result: " + webRequest.downloadHandler.text);
		else
			print(webRequest.error);
	}

	[Serializable]
	class Vector3Value : Value<_Vector3>
	{
		public Vector3Value (string objectName, string valueName, _Vector3 value) : base (objectName, valueName, value)
		{
		}
	}

	[Serializable]
	class Value<T>
	{
		public string objectName;
		public string valueName;
		public T value;

		public Value (string objectName, string valueName, T value)
		{
			this.objectName = objectName;
			this.valueName = valueName;
			this.value = value;
		}
	}

	[Serializable]
	class _Vector3
	{
		public float x;
		public float y;
		public float z;

		public _Vector3 (float x, float y, float z)
		{
			this.x = x;
			this.y = y;
			this.z = z;
		}
	}
}