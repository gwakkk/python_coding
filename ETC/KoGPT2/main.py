import torch
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel
from pydantic import BaseModel, Field

tokenizer = PreTrainedTokenizerFast.from_pretrained(
    "skt/kogpt2-base-v2",
    bos_token='</s>',
    eos_token='</s>',
    unk_token='<unk>',
    pad_token='<pad>',
    mask_token='<mask>') 

model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')


class TextGenerationInput(BaseModel):
    text: str = Field(
        title='Text Input',
        max_length=128,
    )
    max_length: int = Field(
        128,
        ge=5,
        le=128,
    )
    repetition_penalty: float = Field(
        2.0,
        ge=0.0,
        le=2.0,
    )


class TextGenerationOutput(BaseModel):
    generated_text: str = Field(...)
