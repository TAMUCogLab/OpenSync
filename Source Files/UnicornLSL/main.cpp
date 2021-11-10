#include "stdafx.h"
#include <iostream>
#include <fstream>
#include <lsl_cpp.h>
#include <vector>

// Include unicorn header-file.
#include "unicorn.h"

// Include unicorn lib.
#pragma comment(lib, "Unicorn.lib")

// Specifications for the data acquisition.
//-------------------------------------------------------------------------------------
#define DATA_FILE				"data.bin"		// The name of the file which is storing acquired data.
#define ACQUISITION_DURATION_S	10.0f			// The acquisition duration in seconds.
#define FRAME_LENGTH			1				// The number of samples acquired per get data call.
#define TESTSIGNAL_ENABLED		FALSE			// Flag to enable or disable testsignal.

// Function declarations.
//-------------------------------------------------------------------------------------
void HandleError(int errorCode);
void PrintErrorMessage(int errorCode);

//-------------------------------------------------------------------------------------
// Main. Program entry point.
//-------------------------------------------------------------------------------------


lsl::stream_info info("UnicornEEG", "EEG", 17, lsl::cf_float32);
lsl::stream_outlet outlet(info);


struct EEG_Data {

	float ch[17];
};

int main()
{

	std::cout << "\n\t***Unicorn LSL Application***\n\n" <<
		"\tPsychological and Brain Sciences Department\n\tTexas A&M University\n" <<
		"\tSupport Contact: moeinrazavi@tamu.edu\n\n\n";

	// Variable to store error codes.
	int errorCode = UNICORN_ERROR_SUCCESS;

	// Structure that holds the handle for the currecnt session.
	UNICORN_HANDLE deviceHandle = 0;

	try
	{
		// Get available devices.
		//-------------------------------------------------------------------------------------

		// Get number of available devices.
		unsigned int availableDevicesCount = 0;
		errorCode = UNICORN_GetAvailableDevices(NULL, &availableDevicesCount, TRUE);
		HandleError(errorCode);

		if (availableDevicesCount < 1)
		{
			std::cout << "No device available. Please pair with a Unicorn device first.";
			errorCode = UNICORN_ERROR_GENERAL_ERROR;
			HandleError(errorCode);
		}

		//Get available device serials.
		UNICORN_DEVICE_SERIAL* availableDevices = new UNICORN_DEVICE_SERIAL[availableDevicesCount];
		errorCode = UNICORN_GetAvailableDevices(availableDevices, &availableDevicesCount, TRUE);
		HandleError(errorCode);

		std::cout << "Found Device: " << availableDevices[0] << std::endl;
		/*}*/

		// Request device selection.
		unsigned int deviceId;
		deviceId = 0;

		/*HandleError(errorCode);*/

		// Open selected device.
		//-------------------------------------------------------------------------------------
		std::cout << "Trying to connect to '" << availableDevices[deviceId] << "'." << std::endl;
		UNICORN_HANDLE deviceHandle;
		errorCode = UNICORN_OpenDevice(availableDevices[deviceId], &deviceHandle);

		HandleError(errorCode);
		std::cout << "Connected to '" << availableDevices[deviceId] << "'." << std::endl;

		// Create a file to store data.
		std::ofstream file(DATA_FILE, std::ios_base::binary);

		float* acquisitionBuffer = NULL;

		// Initialize acquisition members.
		//-------------------------------------------------------------------------------------
		unsigned int numberOfChannelsToAcquire = 0;
		errorCode = UNICORN_GetNumberOfAcquiredChannels(deviceHandle, &numberOfChannelsToAcquire);
		HandleError(errorCode);

		UNICORN_AMPLIFIER_CONFIGURATION configuration;
		errorCode = UNICORN_GetConfiguration(deviceHandle, &configuration);
		HandleError(errorCode);

		int samplingRate = UNICORN_SAMPLING_RATE;

		// Print acquisition configuration
		std::cout << std::endl;
		std::cout << "Acquisition Configuration:" << std::endl;
		std::cout << "Sampling Rate: " << samplingRate << "Hz" << std::endl;
		std::cout << "Frame Length: " << FRAME_LENGTH << std::endl;
		std::cout << "Number Of Acquired Channels: " << numberOfChannelsToAcquire << std::endl;

		// Allocate memory for the acquisition buffer.
		int acquisitionBufferLength = numberOfChannelsToAcquire * FRAME_LENGTH;
		acquisitionBuffer = new float[acquisitionBufferLength];



		try
		{
			// Start data acquisition.
			//-------------------------------------------------------------------------------------
			errorCode = UNICORN_StartAcquisition(deviceHandle, TESTSIGNAL_ENABLED);
			HandleError(errorCode);
			std::cout << std::endl << "Now started streaming data to LSL..." << std::endl;

			// Calculate number of get data calls.
			int numberOfGetDataCalls = (int)(ACQUISITION_DURATION_S * (samplingRate / FRAME_LENGTH));

			// Limit console update rate to max. 25Hz or slower to prevent acquisition timing issues. 
			int consoleUpdateRate = (int)((samplingRate / FRAME_LENGTH) / 25.0f);
			if (consoleUpdateRate == 0)
				consoleUpdateRate = 1;

			// Acquisition loop.
			//-------------------------------------------------------------------------------------
			while (true)
			{
				// Receives the configured number of samples from the Unicorn device and writes it to the acquisition buffer.
				errorCode = UNICORN_GetData(deviceHandle, FRAME_LENGTH, acquisitionBuffer, acquisitionBufferLength * sizeof(float));
				HandleError(errorCode);

				// Write data to file.
				EEG_Data sample;
				std::vector<EEG_Data> EEG_sample;
				sample.ch[0] = acquisitionBuffer[0];
				sample.ch[1] = acquisitionBuffer[1];
				sample.ch[2] = acquisitionBuffer[2];
				sample.ch[3] = acquisitionBuffer[3];
				sample.ch[4] = acquisitionBuffer[4];
				sample.ch[5] = acquisitionBuffer[5];
				sample.ch[6] = acquisitionBuffer[6];
				sample.ch[7] = acquisitionBuffer[7];
				sample.ch[8] = acquisitionBuffer[8];
				sample.ch[9] = acquisitionBuffer[9];
				sample.ch[10] = acquisitionBuffer[10];
				sample.ch[11] = acquisitionBuffer[11];
				sample.ch[12] = acquisitionBuffer[12];
				sample.ch[13] = acquisitionBuffer[13];
				sample.ch[14] = acquisitionBuffer[14];
				sample.ch[15] = acquisitionBuffer[15];
				sample.ch[16] = acquisitionBuffer[16];

				EEG_sample.push_back(sample);
				outlet.push_chunk_numeric_structs(EEG_sample);
			}

			// Stop data acquisition.
			//-------------------------------------------------------------------------------------
			errorCode = UNICORN_StopAcquisition(deviceHandle);
			HandleError(errorCode);
			std::cout << std::endl << "Data acquisition stopped." << std::endl;
		}
		catch (int errorCode)
		{
			// Write error message to console if something goes wrong.
			PrintErrorMessage(errorCode);
		}
		catch (...)
		{
			// Write error message to console if something goes wrong.
			std::cout << std::endl << "An unknown error occurred." << std::endl;
		}

		// Free memory of the acquisition buffer if necessary.
		if (acquisitionBuffer != NULL)
		{
			delete[] acquisitionBuffer;
			acquisitionBuffer = NULL;
		}

		// Free memory of the device buffer if necessary.
		if (availableDevices != NULL)
		{
			delete[] availableDevices;
			availableDevices = NULL;
		}

		// Close file.
		file.close();

		// Close device.
		//-------------------------------------------------------------------------------------
		errorCode = UNICORN_CloseDevice(&deviceHandle);
		HandleError(errorCode);
		std::cout << "Disconnected from Unicorn." << std::endl;
	}
	catch (int errorCode)
	{
		// Write error message to console if something goes wrong.
		PrintErrorMessage(errorCode);
	}
	catch (...)
	{
		// Write error message to console if something goes wrong.
		std::cout << std::endl << "An unknown error occurred." << std::endl;
	}

	std::cout << std::endl << "Press ENTER to terminate the application.";
	std::cin.clear();
	std::cin.ignore();
	getchar();
	return 0;
}

// The method throws an exception and forwards the error code if something goes wrong.
//-------------------------------------------------------------------------------------
void HandleError(int errorCode)
{
	if (errorCode != UNICORN_ERROR_SUCCESS)
	{
		throw errorCode;
	}
}

// The method prints an error messag to the console according to the error code.
//-------------------------------------------------------------------------------------
void PrintErrorMessage(int errorCode)
{
	std::cout << std::endl << "An error occurred. Error Code: " << errorCode << " - ";
	std::cout << UNICORN_GetLastErrorText();
	std::cout << std::endl;
}