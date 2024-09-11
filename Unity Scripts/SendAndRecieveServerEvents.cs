using System;
using UnityEngine;
using System.Collections;
using UnityEngine.Networking;

public class SendAndRecieveServerEvents : MonoBehaviour
{
	public float pollInterval = 0.1f;
	public static int clientId = -1;
	float pollTimer;

	void Start ()
	{
		StartCoroutine(JoinEvent ());
	}

	void OnDestroy ()
	{
		StartCoroutine(LeftEvent ());
	}

	void Update ()
	{
		if (Input.GetMouseButtonDown(0))
		{
			Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
			RaycastHit hit;
			if (Physics.Raycast(ray.origin, ray.direction, out hit, Mathf.Infinity, 1 << 31, QueryTriggerInteraction.Collide))
				StartCoroutine(ClickEvent (hit.collider.name));
		}
		pollTimer -= Time.deltaTime;
		if (pollTimer <= 0)
		{
			StartCoroutine(PollEvent ());
			pollTimer += pollInterval;
		}
	}
	
	IEnumerator PollEvent ()
	{
		UnityWebRequest webRequest = UnityWebRequest.Get("http://localhost:8000/poll?" + clientId + '?');
		yield return webRequest.SendWebRequest();
		if (webRequest.result == UnityWebRequest.Result.Success)
		{
			string result = webRequest.downloadHandler.text;
			print("Web request result: " + result);
			foreach (string line in result.Split('\n', StringSplitOptions.RemoveEmptyEntries))
			{
				Vector3Value vector3Value = JsonUtility.FromJson<Vector3Value>(line.Replace('\'', '\"'));
				if (vector3Value.objectName != name && vector3Value.valueName == "location")
					GameObject.Find(vector3Value.objectName).transform.position = vector3Value.value.ToVec3();
			}
		}
		else
			print(webRequest.error);
	}
	
	IEnumerator JoinEvent ()
	{
		UnityWebRequest webRequest = UnityWebRequest.Get("http://localhost:8000/join??");
		yield return webRequest.SendWebRequest();
		if (webRequest.result == UnityWebRequest.Result.Success)
		{
			clientId = int.Parse(webRequest.downloadHandler.text);
			print("Web request result: " + clientId);
		}
		else
			print(webRequest.error);
	}
	
	IEnumerator LeftEvent ()
	{
		UnityWebRequest webRequest = UnityWebRequest.Get("http://localhost:8000/left?" + clientId + '?');
		yield return webRequest.SendWebRequest();
		if (webRequest.result == UnityWebRequest.Result.Success)
			print("Web request result: " + webRequest.downloadHandler.text);
		else
			print(webRequest.error);
	}

	IEnumerator ClickEvent (string objectName)
	{
		UnityWebRequest webRequest = UnityWebRequest.Get("http://localhost:8000/click?" + clientId + '?' + objectName);
		yield return webRequest.SendWebRequest();
		if (webRequest.result == UnityWebRequest.Result.Success)
			print("Web request result: " + webRequest.downloadHandler.text);
		else
			print(webRequest.error);
	}

	public static IEnumerator JsonEvent (object obj)
	{
		string jsonText = JsonUtility.ToJson(obj);
		UnityWebRequest webRequest = UnityWebRequest.Get("http://localhost:8000/exec?" + clientId + '?' + jsonText.Base64Encode());
		yield return webRequest.SendWebRequest();
		if (webRequest.result == UnityWebRequest.Result.Success)
			print("Web request result: " + webRequest.downloadHandler.text);
		else
			print(webRequest.error);
	}

	[Serializable]
	public class Vector3Value : Value<_Vector3>
	{
		public Vector3Value (string objectName, string valueName, _Vector3 value) : base (objectName, valueName, value)
		{
		}
	}

	[Serializable]
	public class Value<T>
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
	public class _Vector3
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

		public _Vector3 (Vector3 v) : this (v.x, v.y, v.z)
		{
		}

		public Vector3 ToVec3 ()
		{
			return new Vector3(x, y, z);
		}
	}
}