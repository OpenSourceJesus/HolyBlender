using System;
using System.Net;
using UnityEngine;
using System.Collections;
using System.Net.Sockets;
using UnityEngine.Networking;

public class SendAndRecieveServerEvents : MonoBehaviour
{
	public float pollInterval = .05f;
	float pollTimer;
	string ipAddress;

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
			Vector3Value value = new Vector3Value("Cube", "location", new _Vector3(GameObject.Find("Cube").transform.position));
			StartCoroutine(JsonEvent (value));
			pollTimer += pollInterval;
		}
	}
	
	IEnumerator JoinEvent ()
	{
		ipAddress = GetLocalIPAddress();
		UnityWebRequest webRequest = UnityWebRequest.Get("http://localhost:8000/join?" + ipAddress + '?');
		yield return webRequest.SendWebRequest();
		if (webRequest.result == UnityWebRequest.Result.Success)
			print("Web request result: " + webRequest.downloadHandler.text);
		else
			print(webRequest.error);
	}
	
	IEnumerator LeftEvent ()
	{
		ipAddress = GetLocalIPAddress();
		UnityWebRequest webRequest = UnityWebRequest.Get("http://localhost:8000/left?" + ipAddress + '?');
		yield return webRequest.SendWebRequest();
		if (webRequest.result == UnityWebRequest.Result.Success)
			print("Web request result: " + webRequest.downloadHandler.text);
		else
			print(webRequest.error);
	}

	IEnumerator ClickEvent (string objectName)
	{
		UnityWebRequest webRequest = UnityWebRequest.Get("http://localhost:8000/click?" + ipAddress + '?' + objectName);
		yield return webRequest.SendWebRequest();
		if (webRequest.result == UnityWebRequest.Result.Success)
			print("Web request result: " + webRequest.downloadHandler.text);
		else
			print(webRequest.error);
	}


	IEnumerator JsonEvent (object obj)
	{
		string jsonText = JsonUtility.ToJson(obj);
		UnityWebRequest webRequest = UnityWebRequest.Get("http://localhost:8000/exec?" + ipAddress + '?' + jsonText.Base64Encode());
		yield return webRequest.SendWebRequest();
		if (webRequest.result == UnityWebRequest.Result.Success)
			print("Web request result: " + webRequest.downloadHandler.text);
		else
			print(webRequest.error);
	}

	public static string GetLocalIPAddress ()
	{
		IPHostEntry host = Dns.GetHostEntry(Dns.GetHostName());
		foreach (var ip in host.AddressList)
		{
			if (ip.AddressFamily == AddressFamily.InterNetwork)
				return ip.ToString();
		}
		throw new Exception("No network adapters with an IPv4 address in the system!");
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

		public _Vector3 (Vector3 v) : this (v.x, v.y, v.z)
		{
		}
	}
}