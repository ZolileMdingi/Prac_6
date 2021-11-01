`timescale 1ns / 1ps

module CU
  #(parameter DATA_WIDTH = 8, //8 bit wide data
    parameter ADDR_BITS = 5, //32 Addresses
    parameter INSTR_WIDTH =20 )(
    //De itten during instantiation
    
    //INPUTS
    input clk,rst,
    input [INSTR_WIDTH-1:0]instr,
    input [DATA_WIDTH-1:0] result2,
    //OUTPUTS
    output reg [DATA_WIDTH-1:0] operand1,
    output reg [DATA_WIDTH-1:0] operand2,
    output reg [DATA_WIDTH-1:0] offset,
    output reg [3:0] opcode,
    output reg [DATA_WIDTH-1:0] CUregisters [3:0],
    output reg sel1, sel3, w_r
    );

    //REGISTER FILE: CU internal register file of 4 registers.  This is a over simplication of a real solution
    reg [DATA_WIDTH-1:0] regfile [3:0];
    reg [INSTR_WIDTH-1:0]instruction;
    
    //STATES
    parameter RESET = 4'b0000;
    parameter DECODE = 4'b0001;
    parameter EXECUTE = 4'b0010;
    parameter MEM_ACCESS = 4'b0100;
    parameter WRITE_BACK = 4'b1000;
        
    reg [3:0] state = RESET;
 
  
    
    always @(posedge clk) begin
        instruction = instr;
      
        case (state)
            RESET : begin //#0
                if (instruction[19:18] == 2'b00)  begin
                    state = RESET; 
                    end else begin
                    state = DECODE; //#1
                    end
                //-----------------------------
                //Write initial values to regfile
                regfile[0]<= 8'd0;
                regfile[1]<= 8'd1;
                regfile[2]<= 8'd2;
                regfile[3]<= 8'd3;
				CUregisters[0] <= regfile[0];
              CUregisters[1] <= regfile[1];
              CUregisters[2] <= regfile[2];
              CUregisters[3] <= regfile[3];
                //Set output reset defaults
                operand1 <= #(DATA_WIDTH)'d0;
                operand2 <= #(DATA_WIDTH)'d0;
                offset <= #(DATA_WIDTH)'d0;
                opcode <= 4'b1111;
                sel1 <= 0;
                sel3 <= 0;
                w_r <= 0;
                //-----------------------------
            end

            DECODE : begin //#1 
              CUregisters[0] <= regfile[0];
              CUregisters[1] <= regfile[1];
              CUregisters[2] <= regfile[2];
              CUregisters[3] <= regfile[3];
                state = EXECUTE; //#2
                if (instruction[19:18] == 2'b1) begin //std_op
                    operand1 <= regfile[instruction[15:14]]; //X2
                    operand2 <= regfile[instruction[13:12]]; //X3
                    offset <= instruction[11:4];
                    opcode <= instruction[3:0];
                   sel1 <= 1;
                    sel3 <= 0;
                    w_r <= 0;
                end else if (instruction[19:18] == 2'b10) begin //loadR 
                    operand1 <= regfile[instruction[15:14]]; //X2
                    operand2 <= regfile[instruction[17:16]]; //z
                    offset <= instruction[11:4];
                    opcode <= instruction[3:0];
                    sel1 <= 0; //pass data_out
                    sel3 <= 1; //pass offset
                    w_r <= 0;
                end else if (instruction[19:18] == 2'b11) begin //storeR 
                   /******************************************** 
                   *
                   * FILL IN CORRECT CODE HERE
                   *
                   ********************************************/ 
                    operand1 <= regfile[instruction[15:14]]; //X2
                    operand2 <= regfile[instruction[17:16]]; //X1
                    offset <= instruction[11:4];
                    opcode <= instruction[3:0];
                    sel1 <= 1; //pass data_out
                    sel3 <= 1; //pass offset
                    w_r <= 1;

                end
            end
            EXECUTE: begin //#2
              CUregisters[0] <= regfile[0];
              CUregisters[1] <= regfile[1];
              CUregisters[2] <= regfile[2];
              CUregisters[3] <= regfile[3];
                state = MEM_ACCESS; //#3
                if (instruction[19:18] == 2'b01) begin //std_op
                    state = WRITE_BACK;
                    operand1 <= regfile[instruction[15:14]]; //X2
                    operand2 <= regfile[instruction[13:12]]; //X3
                    offset <= instruction[11:4];
                    opcode <= instruction[3:0];
                    sel1 <= 1;
                    sel3 <= 0;
                    w_r <= 0;

                end else if (instruction[19:18] == 2'b10) begin //loadR  
                    operand1 <= regfile[instruction[15:14]]; //X2
                    operand2 <= regfile[instruction[17:16]]; //z
                    offset <= instruction[11:4];
                    opcode <= instruction[3:0];
                    sel1 <= 0; //pass data_out
                    sel3 <= 1; //pass offset
                    w_r <= 0;
                end else if (instruction[19:18] == 2'b11) begin //storeR
                   /******************************************** 
                   *
                   * FILL IN CORRECT CODE HERE
                   *
                   ********************************************/ 
                    operand1 <= regfile[instruction[15:14]]; //X2
                    operand2 <= regfile[instruction[17:16]]; //X1
                    offset <= instruction[11:4];
                    opcode <= instruction[3:0];
                    sel1 <= 1; //pass data_out
                    sel3 <= 1; //pass offset
                    w_r <= 1;
                end
            end
            MEM_ACCESS: begin //#3
              CUregisters[0] <= regfile[0];
              CUregisters[1] <= regfile[1];
              CUregisters[2] <= regfile[2];
              CUregisters[3] <= regfile[3];
                state = WRITE_BACK; //#4
                if (instruction[19:18] == 2'b10) begin //loadR             
                    operand1 <= regfile[instruction[15:14]]; //X2
                    operand2 <= regfile[instruction[17:16]]; //z
                    offset <= instruction[11:4];
                    opcode <= instruction[3:0];
                    sel1 <= 0; //pass data_out
                    sel3 <= 1; //pass offset
                    w_r <= 0;
                end else if (instruction[19:18] == 2'b11) begin //storeR 
                   /******************************************** 
                   *
                   * FILL IN CORRECT CODE HERE
                   * Take note of what the next state should be according to
                   * the FSM
                   *
                   ********************************************/ 
                    state = DECODE;
                    operand1 <= regfile[instruction[15:14]]; //X2
                    operand2 <= regfile[instruction[17:16]]; //X1
                    offset <= instruction[11:4];
                    opcode <= instruction[3:0];
                    sel1 <= 1; //pass data_out
                    sel3 <= 1; //pass offset
                    w_r <= 1;
                end
            end
            WRITE_BACK: begin //#4
              CUregisters[0] <= regfile[0];
              CUregisters[1] <= regfile[1];
              CUregisters[2] <= regfile[2];
              CUregisters[3] <= regfile[3];
                state = DECODE; //#1
                if (instruction[19:18] == 2'b01) begin //std_op
                    regfile[instruction[17:16]] <= result2; //X1

                    operand1 <= regfile[instruction[15:14]]; //X2
                    operand2 <= regfile[instruction[13:12]]; //X3
                    offset <= instruction[11:4];
                    opcode <= instruction[3:0];
                    sel1 <= 1;
                    sel3 <= 0;
                    w_r <= 0;
                end else if (instruction[19:18] == 2'b11) begin //storeR 
                   /******************************************** 
                   *
                   * FILL IN CORRECT CODE HERE
                   *
                   ********************************************/ 
                    state = DECODE; 
                    
                end else if (instruction[19:18] == 2'b10) begin //loadR             
                    regfile[instruction[17:16]] <= result2; //From data mem
                    operand1 <= regfile[instruction[15:14]]; //X2
                    operand2 <= regfile[instruction[17:16]]; //z
                    offset <= instruction[11:4];
                    opcode <= instruction[3:0];
                    sel1 <= 0; //pass data_out
                    sel3 <= 1; //pass offset
                    w_r <= 0;
                end
            end
			
            default: // Fault Recovery
            state = RESET; //#0
          
        endcase
    end
endmodule