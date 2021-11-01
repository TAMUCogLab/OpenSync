using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using System;
using System.IO;
using Valve.VR;


[CustomEditor(typeof(OpenSync))]

public class OpenSync_Editor : Editor
{
    SerializedProperty unicorn;
    SerializedProperty liveamp;
    SerializedProperty openbci;
    SerializedProperty mindwave;
    SerializedProperty muse;
    SerializedProperty kinectbodybasics;
    SerializedProperty gazepoint;
    SerializedProperty vive;
    SerializedProperty vive_controller;
    SerializedProperty save_path;

    // is called once when according object gains focus in the hierachy
    private void OnEnable()
    {
        // link serialized properties to the target's fields
        // more efficient doing this only once
        unicorn = serializedObject.FindProperty("Unicorn");
        liveamp = serializedObject.FindProperty("LiveAmp");
        openbci = serializedObject.FindProperty("OpenBCI");
        mindwave = serializedObject.FindProperty("Mindwave");
        muse = serializedObject.FindProperty("Muse");
        kinectbodybasics = serializedObject.FindProperty("KinectBodyBasics");
        gazepoint = serializedObject.FindProperty("Gazepoint");
        vive = serializedObject.FindProperty("ViVE");
        vive_controller = serializedObject.FindProperty("ViVEController");
        save_path = serializedObject.FindProperty("Save_Path");
    }

    public override void OnInspectorGUI()
    {

        // fetch current values from the real instance into the serialized "clone"
        serializedObject.Update();

        OpenSync script = (OpenSync)target;
        // Draw field for different devices

        GUIContent Unicorn = new GUIContent("g.tec Unicorn");
        GUIContent LiveAmp = new GUIContent("BrainProducts LiveAmp");
        GUIContent OpenBCI = new GUIContent("OpenBCI");
        GUIContent OpenBCI_Board = new GUIContent("    Board");
        GUIContent Mindwave = new GUIContent("Neurosky Mindwave");
        GUIContent Muse = new GUIContent("Muse");
        GUIContent Kinect = new GUIContent("Kinect");
        GUIContent GazePoint = new GUIContent("GazePoint");
        GUIContent BioMetrics = new GUIContent("    Record BioMetrics?");
        GUIContent ViVE = new GUIContent("HTC ViVE");
        GUIContent ViVE_Controller = new GUIContent("ViVE Controller");
        GUIContent ViVE_Controller_Hand = new GUIContent("    Controller Hand");

        EditorGUILayout.PropertyField(unicorn, Unicorn);
        EditorGUILayout.PropertyField(liveamp, LiveAmp);



        GUIContent SRate = new GUIContent("    Sampling Rate");
        GUIContent N_Channels = new GUIContent("    Number of Channels");
        GUIContent Save_Path = new GUIContent("    Save Path");
        GUIContent Recording = new GUIContent("Recording?");

        if (liveamp.boolValue)
        {
            script.SRateIdx = EditorGUILayout.Popup(SRate, script.SRateIdx, script.SRate);
            script.ChannelIdx = EditorGUILayout.Popup(N_Channels, script.ChannelIdx, script.N_Channels);
        }

        EditorGUILayout.PropertyField(openbci, OpenBCI);
        if (openbci.boolValue)
        {
            script.BoardIdx = EditorGUILayout.Popup(OpenBCI_Board, script.BoardIdx, script.Board);
        }

        EditorGUILayout.PropertyField(mindwave, Mindwave);
        EditorGUILayout.PropertyField(muse, Muse);
        EditorGUILayout.PropertyField(kinectbodybasics, Kinect);

        EditorGUILayout.PropertyField(gazepoint, GazePoint);
        if (gazepoint.boolValue)
        {
            script.BioIdx = EditorGUILayout.Popup(BioMetrics, script.BioIdx, script.BioMetrics);
        }

        EditorGUILayout.PropertyField(vive, ViVE);


        EditorGUILayout.PropertyField(vive_controller, ViVE_Controller);

        if (vive_controller.boolValue)
        {
            script.HandIdx = EditorGUILayout.Popup(ViVE_Controller_Hand, script.HandIdx, script.HandType);
        }

        EditorGUILayout.LabelField("", EditorStyles.boldLabel);
        EditorGUILayout.LabelField("Record", EditorStyles.boldLabel);
        script.RecIdx = EditorGUILayout.Popup(Recording, script.RecIdx, script.Recording);

        if (script.RecIdx == 1)
        {
            script.Save_Path = EditorGUILayout.TextField(Save_Path, script.Save_Path);
        }
        //base.OnInspectorGUI();


        // write back serialized values to the real instance
        // automatically handles all marking dirty and undo/redo
        serializedObject.ApplyModifiedProperties();
    }
}