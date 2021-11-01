using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using System;
using System.IO;
using System.Diagnostics;
using Valve.VR;
using Assets.LSL4Unity.Scripts; // reference the namespace to get access to all classes
using LSL;

public class OpenSync : MonoBehaviour
{


    // Start is called before the first frame update
    [Header("EEG Devices")]
    public bool Unicorn;

    public bool LiveAmp;
    public string[] SRate = new string[] { "250", "500", "1000" };
    public int SRateIdx = 0;
    public string[] N_Channels = new string[] { "16", "32", "64" };
    public int ChannelIdx = 0;

    public bool OpenBCI;
    public string[] Board = new string[] { "Cyton", "Cyton + Daisy" };
    public int BoardIdx = 0;

    public bool Mindwave;

    public bool Muse;

    [Header("Body Motion")]
    public bool KinectBodyBasics;
    [Header("Eye-Tracking")]
    public bool Gazepoint;
    public string[] BioMetrics = new string[] { "No", "Yes" };
    public int BioIdx = 0;

    public bool ViVE;

    [Header("I/O")]
    public bool ViVEController;
    public string[] HandType = new string[] { "Right-Hand Controller", "Left-Hand Controller", "Both Hands Controllers" };
    public int HandIdx = 0;

    private SteamVR_ActionSet actionSet = SteamVR_Input.GetActionSet("default");

    private SteamVR_Input_Sources forSources = SteamVR_Input_Sources.Any;

    private bool disableAllOtherActionSets = false;

    private bool activateOnStart = true;
    private bool deactivateOnDestroy = true;
    // a reference to the action
    private SteamVR_Action_Boolean Right_Hand_Trigger_Data;
    private SteamVR_Action_Boolean Left_Hand_Trigger_Data;
    // a reference to the hand
    private SteamVR_Input_Sources right_hand_controller = SteamVR_Input_Sources.RightHand;
    private SteamVR_Input_Sources left_hand_controller = SteamVR_Input_Sources.LeftHand;


    private const string righthand_lsl_id = "Right-Hand_Controller_ID";

    private string righthand_lslStreamName = "Right-Hand Controller";
    private string righthand_lslStreamType = "Marker";

    private liblsl.StreamInfo righthand_lslStreamInfo;
    private liblsl.StreamOutlet righthand_lslOutlet;
    private int righthand_lslChannelCount = 1;


    private const string lefthand_lsl_id = "Left-Hand_Controller_ID";

    private string lefthand_lslStreamName = "Left-Hand Controller";
    private string lefthand_lslStreamType = "Marker";

    private liblsl.StreamInfo lefthand_lslStreamInfo;
    private liblsl.StreamOutlet lefthand_lslOutlet;
    private int lefthand_lslChannelCount = 1;

    //Assuming that markers are never send in regular intervalls

    //Assuming that markers are never send in regular intervalls
    private double nominal_srate = liblsl.IRREGULAR_RATE;

    private const liblsl.channel_format_t lslChannelFormat = liblsl.channel_format_t.cf_string;

    private string[] righthand_sample;
    private string[] lefthand_sample;


    //private LSLMarkerStream Trigger_Marker;
    private bool Right_Trigger_Last_State = false;  // When the trigger is pressed, Trigger_Last_State is "true" otherwise "false"
    private bool Left_Trigger_Last_State = false;  // When the trigger is pressed, Trigger_Last_State is "true" otherwise "false"


    [Header("Recording")]
    public string[] Recording = new string[] { "No", "Yes" };
    public int RecIdx = 0;

    public string Save_Path = @"C:\Users\" + Environment.UserName + @"\Desktop\Unity_Data\";

    private bool start_flag = true;

    void Awake()
    {
        if (ViVEController) { 
            if (HandIdx == 0)
            {
                righthand_sample = new string[lefthand_lslChannelCount];

                righthand_lslStreamInfo = new liblsl.StreamInfo(
                                            righthand_lslStreamName,
                                            righthand_lslStreamType,
                                            righthand_lslChannelCount,
                                            nominal_srate,
                                            lslChannelFormat,
                                            righthand_lsl_id);

                righthand_lslOutlet = new liblsl.StreamOutlet(righthand_lslStreamInfo);
            }

            if (HandIdx == 1)
            {
                lefthand_sample = new string[lefthand_lslChannelCount];

                lefthand_lslStreamInfo = new liblsl.StreamInfo(
                                            lefthand_lslStreamName,
                                            lefthand_lslStreamType,
                                            lefthand_lslChannelCount,
                                            nominal_srate,
                                            lslChannelFormat,
                                            lefthand_lsl_id);

                lefthand_lslOutlet = new liblsl.StreamOutlet(lefthand_lslStreamInfo);
            }

            if (HandIdx == 2)
            {
                righthand_sample = new string[lefthand_lslChannelCount];

                righthand_lslStreamInfo = new liblsl.StreamInfo(
                                            righthand_lslStreamName,
                                            righthand_lslStreamType,
                                            righthand_lslChannelCount,
                                            nominal_srate,
                                            lslChannelFormat,
                                            righthand_lsl_id);

                righthand_lslOutlet = new liblsl.StreamOutlet(righthand_lslStreamInfo);

                lefthand_sample = new string[lefthand_lslChannelCount];

                lefthand_lslStreamInfo = new liblsl.StreamInfo(
                                            lefthand_lslStreamName,
                                            lefthand_lslStreamType,
                                            lefthand_lslChannelCount,
                                            nominal_srate,
                                            lslChannelFormat,
                                            lefthand_lsl_id);

                lefthand_lslOutlet = new liblsl.StreamOutlet(lefthand_lslStreamInfo);
            }
        }
    }

    private void Start()
    {
        if (start_flag)
        {
            start_flag = false;
            if (actionSet != null && activateOnStart)
            {
                actionSet.Activate(forSources, 0, disableAllOtherActionSets);
            }

            string strCmdText;
            string curr_day = System.DateTime.Now.Day.ToString();
            string curr_mon = System.DateTime.Now.Month.ToString();
            string curr_year = System.DateTime.Now.Year.ToString();
            string curr_hour = System.DateTime.Now.Hour.ToString();
            string curr_min = System.DateTime.Now.Minute.ToString();
            string curr_sec = System.DateTime.Now.Second.ToString();
            string curr_time = curr_mon + "-" + curr_day + "-" + curr_year + "_" + curr_hour + "-" + curr_min + "-" + curr_sec;

            //###################################
            //############# EEG LSL #############
            //###################################

            if (Unicorn)
            {
                //""" Run Unicorn LSL -- Sending Unicorn Data to LSL """
                System.Diagnostics.Process.Start("CMD.exe", @"/C .\Assets\UnicornLSL\UnicornLSL.exe");
            }
            if (LiveAmp)
            {
                //""" Run BrainProducts LiveAmp - 16 Channel LSL -- Send LiveAmp Data to LSL """
                System.Diagnostics.Process.Start("CMD.exe", @"/C .\Assets\LiveAmpLSL\LiveAmp-LSL.exe" + " " + N_Channels[ChannelIdx] + " " + SRate[SRateIdx]);
            }
            if (OpenBCI)
            {
                //""" Run OpenBCI Send Data to LSL """
                if (BoardIdx == 1)
                {
                    System.Diagnostics.Process.Start("CMD.exe", @"/C python .\Assets\OpenBCILSL\OpenBCILSL_Daisy.py");
                }
                else
                {
                    System.Diagnostics.Process.Start("CMD.exe", @"/C python .\Assets\OpenBCILSL\OpenBCILSL.py");
                }

            }

            if (Mindwave)
            {
                //""" Send Mindwave data to LSL -- 
                //Remember to install Mindwave LSL using: pip install mindwavelsl """
                System.Diagnostics.Process.Start("CMD.exe", @"/C python .\Assets\MindwaveLSL\mindwave_LSL.py");
            }
            if (Muse)
            {
                //""" Send Muse data to LSL """
                //""" Download and Install Bluemuse from:
                //    https://github.com/kowalej/BlueMuse/releases/download/v2.1/BlueMuse_2.1.0.0.zip
                //        1.Navigate to the unzipped app folder and run the .\InstallBlueMuse.ps1 PowerShell
                //            command(right click and choose Run with PowerShell or execute from terminal directly):
                //        2.Follow the prompts -the script should automatically
                //          install the security certificate, all dependencies, and the BlueMuse app.
                //    Reference: https://github.com/kowalej/BlueMuse """
                //# Set LSL_LOCAL_CLOCK for MUSE and Send Muse Data to LSL
                System.Diagnostics.Process.Start("CMD.exe", "/C start bluemuse://setting?key=primary_timestamp_format!value=LSL_LOCAL_CLOCK_NATIVE");
                System.Diagnostics.Process.Start("CMD.exe", "/C start bluemuse://start?streamfirst=true");
            }

            //##################################################
            //############# KINECT BODY BASICS LSL #############
            //##################################################
            //""" Run Kinect Body Basics LSL -- Sending kinect Body Basics Data to LSL """
            //""" Remember to Download and Install Microsoft Kinect for Windows SDK 2.0 from:
            //    https://www.microsoft.com/en-us/download/details.aspx?id=44561
            //        Restart your PC after installing Kinect SDK """
            if (KinectBodyBasics)
            {
                System.Diagnostics.Process.Start("CMD.exe", @"/C .\Assets\KinectBodyBasicsLSL\BodyBasicsLSL.exe");
            }

            if (Gazepoint)
            {
                Process[] processes = Process.GetProcessesByName("Gazepoint");
                foreach (var process in processes)
                {
                    process.Kill();
                }

                System.Diagnostics.Process.Start("CMD.exe", @"/C C:\Program Files (x86)\Gazepoint\Gazepoint\bin64\Gazepoint.exe");

                if (BioIdx == 1)
                {
                    System.Diagnostics.Process.Start("CMD.exe", @"/C python .\Assets\GazepointLSL\LSLGazepointBiometrics.py");
                }
                else
                {
                    System.Diagnostics.Process.Start("CMD.exe", @"/C python .\Assets\GazepointLSL\LSLGazepoint.py");
                }
            }

            if (ViVE)
            {
                System.Diagnostics.Process.Start("CMD.exe", @"/C .\Assets\Eyetracking_ViVE\SRanipal_Sample.exe");
            }

            if (RecIdx == 1)
            {
                if (!Directory.Exists(Save_Path)) Directory.CreateDirectory(Save_Path);
                strCmdText = @"/C .\Assets\LabRecorder\LabRecorderCLI.exe " + Save_Path + curr_time + ".xdf 'searchstr'";
                System.Diagnostics.Process.Start("CMD.exe", strCmdText);
            }

            if (ViVEController)
            {
                if (HandIdx == 0)
                {
                    Right_Hand_Trigger_Data.AddOnStateDownListener(RightTriggerDown, right_hand_controller);
                    Right_Hand_Trigger_Data.AddOnStateUpListener(RightTriggerUp, right_hand_controller);
                }
                if (HandIdx == 1)
                {
                    Left_Hand_Trigger_Data.AddOnStateDownListener(LeftTriggerDown, left_hand_controller);
                    Left_Hand_Trigger_Data.AddOnStateUpListener(LeftTriggerUp, left_hand_controller);
                }
                if (HandIdx == 2)
                {
                    Right_Hand_Trigger_Data.AddOnStateDownListener(RightTriggerDown, right_hand_controller);
                    Right_Hand_Trigger_Data.AddOnStateUpListener(RightTriggerUp, right_hand_controller);

                    Left_Hand_Trigger_Data.AddOnStateDownListener(LeftTriggerDown, left_hand_controller);
                    Left_Hand_Trigger_Data.AddOnStateUpListener(LeftTriggerUp, left_hand_controller);
                }
            }
        }
    }

    private void OnDestroy()
    {
        if (actionSet != null && deactivateOnDestroy)
        {
            actionSet.Deactivate(forSources);
        }
    }

    public void RightTriggerUp(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource)
    {
        if (Right_Trigger_Last_State == true && ViVEController)
        {
            Right_Trigger_Last_State = false;
            righthand_sample[0] = "Right_Trigger_Released";
            righthand_lslOutlet.push_sample(righthand_sample);
        }
    }
    public void RightTriggerDown(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource)
    {
        if (Right_Trigger_Last_State == false && ViVEController)
        {
            Right_Trigger_Last_State = true;
            righthand_sample[0] = "Right_Trigger_Pressed";
            righthand_lslOutlet.push_sample(righthand_sample);
        }
    }


    public void LeftTriggerUp(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource)
    {
        if (Left_Trigger_Last_State == true && ViVEController)
        {
            Left_Trigger_Last_State = false;
            lefthand_sample[0] = "Left_Trigger_Released";
            lefthand_lslOutlet.push_sample(lefthand_sample);
        }
    }
    public void LeftTriggerDown(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource)
    {
        if (Left_Trigger_Last_State == false && ViVEController)
        {
            Left_Trigger_Last_State = true;
            lefthand_sample[0] = "Left_Trigger_Pressed";
            lefthand_lslOutlet.push_sample(lefthand_sample);
        }
    }

    // Update is called once per frame
    private void Update()
    {

    }
}