using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using UnityEngine.SceneManagement;

namespace HolyBlender
{
	public class _SceneManager : SingletonMonoBehaviour<_SceneManager>
	{
		public float transitionRate;
		public static bool isLoading;
		public static Scene CurrentScene
		{
			get
			{
				return SceneManager.GetActiveScene();
			}
		}

		public override void Awake ()
		{
			base.Awake ();
			isLoading = false;
		}
		
		public void LoadScene (string sceneName)
		{
			isLoading = true;
			SceneManager.LoadScene(sceneName);
		}
		
		public void LoadScene (int sceneId)
		{
			isLoading = true;
			SceneManager.LoadScene(sceneId);
		}
		
		public void LoadSceneAdditive (string sceneName)
		{
			isLoading = true;
			SceneManager.LoadScene(sceneName, LoadSceneMode.Additive);
		}
		
		public void LoadSceneAdditive (int sceneId)
		{
			isLoading = true;
			SceneManager.LoadScene(sceneId, LoadSceneMode.Additive);
		}
		
		public AsyncOperation LoadSceneAsyncAdditive (string sceneName)
		{
			isLoading = true;
			return SceneManager.LoadSceneAsync(sceneName, LoadSceneMode.Additive);
		}
		
		public AsyncOperation LoadSceneAsyncAdditive (int sceneId)
		{
			isLoading = true;
			return SceneManager.LoadSceneAsync(sceneId, LoadSceneMode.Additive);
		}
		
		public AsyncOperation UnloadSceneAsync (string sceneName)
		{
			return SceneManager.UnloadSceneAsync(sceneName);
		}
		
		public void RestartScene ()
		{
			LoadScene (CurrentScene.name);
		}
		
		public void NextScene ()
		{
			LoadScene (CurrentScene.buildIndex + 1);
		}
		
		public void PreviousScene ()
		{
			LoadScene (CurrentScene.buildIndex - 1);
		}

	}
}