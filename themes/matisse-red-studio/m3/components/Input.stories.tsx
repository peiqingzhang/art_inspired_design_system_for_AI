import type { Meta, StoryObj } from '@storybook/react';
import Input from './Input';

const meta  : Meta<typeof Input> = {
  title: 'Components/Input',
  component: Input,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Input>;

export const Outlined: Story = { args={{ label: 'Email', variant: 'outlined' }} };
export const Filled: Story = { args={{ label: 'Email', variant: 'filled' }} };
