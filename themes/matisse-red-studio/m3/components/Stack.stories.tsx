import type { Meta, StoryObj } from '@storybook/react';
import Stack from './Stack';

const meta  : Meta<typeof Stack> = {
  title: 'Components/Stack',
  component: Stack,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Stack>;

export const Row: Story = { args={{ direction: 'row', children: 'Items' }} };
export const Column: Story = { args={{ direction: 'column', children: 'Items' }} };
