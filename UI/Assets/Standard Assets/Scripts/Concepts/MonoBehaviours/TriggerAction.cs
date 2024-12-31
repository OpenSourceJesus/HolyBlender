using UnityEngine;
using System.Collections;
using UnityEngine.Events;
using UnityEngine.SceneManagement;

namespace HolyBlender
{
	public class TriggerAction : MonoBehaviour
	{
		public UnityEvent action;
		public bool onEnable;
		public bool onAwake;
		public bool onStart;
		public bool onDisable;
		public bool onDestroy;
		public bool onLevelLoaded;
		public bool onLevelUnloaded;
		public bool onTriggerEnter2D;
		public bool onTriggerExit2D;
		public int initTriggersUntilAct = 1;
		int triggersUntilAct;
		bool justRanAwake;
		
	    void OnEnable ()
		{
			if (onEnable)
	        	Trigger ();
		}
		
		void Awake ()
		{
			triggersUntilAct = initTriggersUntilAct;
			if (onAwake)
				Trigger ();
			if (onLevelLoaded)
				SceneManager.sceneLoaded += LevelLoaded;
			if (onLevelUnloaded)
				SceneManager.sceneUnloaded += LevelUnloaded;
			justRanAwake = true;
		}
		
		void Start ()
		{
			if (onStart)
				Trigger ();
			if (justRanAwake)
				return;
			if (onLevelLoaded)
				SceneManager.sceneLoaded += LevelLoaded;
			if (onLevelUnloaded)
				SceneManager.sceneUnloaded += LevelUnloaded;
			justRanAwake = false;
		}
		
		void OnDisable ()
		{
			if (onDisable)
				Trigger ();
		}
		
		void OnDestroy ()
		{
			if (onDestroy)
				Trigger ();
		}
		
		void OnTriggerEnter2D (Collider2D other)
		{
			if (onTriggerEnter2D)
				Trigger ();
		}
		
		void OnTriggerExit2D (Collider2D other)
		{
			if (onTriggerExit2D)
				Trigger ();
		}
		
		void LevelLoaded (Scene scene, LoadSceneMode loadMode)
		{
			if (this != null)
				Trigger ();
		}
		
		void LevelUnloaded (Scene scene)
		{
			if (this != null)
				Trigger ();
		}
		
		public void Trigger ()
		{
			triggersUntilAct --;
			if (triggersUntilAct == 0 && action != null)
				action.Invoke ();
		}
		
		public void Restart (int triggersUntilAct)
		{
			this.triggersUntilAct = triggersUntilAct;
		}
		
		public void Restart ()
		{
			Restart (initTriggersUntilAct);
		}
	}
}